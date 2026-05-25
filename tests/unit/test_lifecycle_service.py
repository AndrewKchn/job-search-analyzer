from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from job_analyzer.models.job_dto import JobDTO
from job_analyzer.models.sync_result import SyncResult
from job_analyzer.services.lifecycle_service import JobLifecycleService


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def mock_lifecycle_service(mock_repo):
    return JobLifecycleService(mock_repo)


@pytest.fixture
def fake_job():
    return JobDTO(
        slug="python-dev",
        company_name="Google",
        title="Python Developer",
        description="Backend work",
        remote=True,
        url="https://example.com",
        tags=["python", "backend"],
        job_types=["full-time"],
        location="Berlin",
        created_at=123456
    )


def test_detect_new_jobs_for_insert(mock_lifecycle_service, fake_job):
    # Act
    result = mock_lifecycle_service._detect_new_jobs_for_insert(
        [fake_job],
        existing_job_ids=set()
    )

    # Assert
    assert len(result) == 1
    assert result[0] == fake_job


def test_detect_new_jobs_excludes_existing(mock_lifecycle_service, fake_job):
    # Act
    result = mock_lifecycle_service._detect_new_jobs_for_insert(
        [fake_job],
        existing_job_ids={fake_job.hash_id}
    )

    # Assert
    assert result == []


def test_detect_existing_jobs_for_update(mock_lifecycle_service, fake_job):
    # Act
    result = mock_lifecycle_service._detect_existing_jobs_for_update(
        [fake_job],
        existing_job_ids={fake_job.hash_id}
    )

    # Assert
    assert result == [fake_job.hash_id]


def test_save_new_jobs(mock_lifecycle_service, mock_repo, fake_job):
    mock_repo.insert_jobs.return_value = 1

    # Act
    result = mock_lifecycle_service._save_new_jobs(
        incoming_jobs=[fake_job],
        existing_job_ids=set(),
        sync_time=100
    )

    # Assert
    assert result == 1

    mock_repo.insert_jobs.assert_called_once_with(
        [fake_job],
        100
    )


def test_save_new_jobs_returns_zero_when_no_new_jobs(
        mock_lifecycle_service,
        mock_repo,
        fake_job
):
    # Act
    result = mock_lifecycle_service._save_new_jobs(
        incoming_jobs=[fake_job],
        existing_job_ids={fake_job.hash_id},
        sync_time=100
    )

    # Assert
    assert result == 0

    mock_repo.insert_jobs.assert_not_called()


def test_update_jobs_timestamps(mock_lifecycle_service, mock_repo, fake_job):
    # Arrange
    mock_repo.touch_jobs.return_value = 1

    # Act
    result = mock_lifecycle_service._update_jobs_timestamps(
        incoming_jobs=[fake_job],
        existing_job_ids={fake_job.hash_id},
        sync_time=100
    )

    # Assert
    assert result == 1

    mock_repo.touch_jobs.assert_called_once_with(
        [fake_job.hash_id],
        100
    )


@patch("job_analyzer.services.lifecycle_service.datetime")
def test_sync_jobs_full_flow(mock_datetime, mock_lifecycle_service, mock_repo, fake_job):
    # Arrange
    fake_now = datetime(2026, 5, 25, 12, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = fake_now
    mock_repo.get_existing_job_ids.return_value = set()

    mock_repo.insert_jobs.return_value = 1
    mock_repo.touch_jobs.return_value = 0
    mock_repo.mark_jobs_inactive.return_value = 2

    # Act
    result = mock_lifecycle_service.sync_jobs([fake_job])

    # Assert
    assert isinstance(result, SyncResult)

    assert result.new_jobs == 1
    assert result.updated_jobs == 0
    assert result.inactive_jobs == 2

    mock_repo.get_existing_job_ids.assert_called_once()
    mock_repo.insert_jobs.assert_called_once()
    mock_repo.touch_jobs.assert_called_once()
    mock_repo.mark_jobs_inactive.assert_called_once_with(fake_now)
