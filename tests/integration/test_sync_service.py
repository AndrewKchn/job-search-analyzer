from unittest.mock import MagicMock, patch

import pytest

from job_analyzer.models.job_dto import JobDTO
from job_analyzer.services.sync_service import SyncService


@pytest.fixture
def fake_job_data():
    return {
        "data": [
            {
                "slug": "python-dev",
                "company_name": "Google",
                "title": "Python Developer",
                "description": "Backend work",
                "remote": True,
                "url": "https://example.com",
                "tags": ["python", "backend"],
                "job_types": ["full-time"],
                "location": "Berlin",
                "created_at": 123456
            }
        ],
        "links": {"next": "https://api.arbeitnow.com/jobs?page=2"}
    }


@pytest.fixture
def mock_lifecycle_service():
    return MagicMock()


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def mock_sync_service(mock_client, mock_lifecycle_service):
    return SyncService(
        client=mock_client,
        job_lifecycle_service=mock_lifecycle_service
    )


@patch('time.sleep', return_value=None)
@patch('job_analyzer.services.sync_service.settings.UPDATE_PAGES_LIMIT', 5)
def test_receive_all_jobs_multiple_pages(mock_sleep, mock_sync_service, mock_client):
    # Arrange
    mock_client.get_jobs_from_page.side_effect = [
        {"data": [{"title": "job1"}], "links": {"next": "page2"}},
        {"data": [{"title": "job2"}], "links": {"next": None}}
    ]

    # Act
    result = mock_sync_service._receive_all_jobs()

    # Assert
    assert len(result) == 2

    assert result[0]["title"] == "job1"
    assert result[1]["title"] == "job2"

    assert mock_client.get_jobs_from_page.call_count == 2


@patch('time.sleep', return_value=None)
def test_sync_jobs_from_all_pages_fetches_multiple_pages(mock_sleep, mock_sync_service, mock_client,
                                                          mock_lifecycle_service, fake_job_data):
    # Arrange
    mock_client.get_jobs_from_page.side_effect = [
        {
            "data": [fake_job_data["data"][0]],
            "links": {"next": "page2"}
        },
        {
            "data": [],
            "links": {"next": None}
        }
    ]

    # Act
    mock_sync_service.sync_jobs_from_all_pages()

    # Assert
    mock_lifecycle_service.sync_jobs.assert_called_once()

    passed_jobs = (
        mock_lifecycle_service
        .sync_jobs
        .call_args[0][0]
    )

    assert len(passed_jobs) == 1

    assert isinstance(passed_jobs[0], JobDTO)

    assert passed_jobs[0].title == "Python Developer"


@patch('time.sleep', return_value=None)
def test_receive_all_jobs_stops_when_no_next(mock_sleep, mock_sync_service, mock_client):
    # Arrange
    mock_client.get_jobs_from_page.return_value = {
        "data": [{"title": "job1"}],
        "links": {"next": None}
    }

    # Act
    result = mock_sync_service._receive_all_jobs()

    # Assert
    assert len(result) == 1

    mock_client.get_jobs_from_page.assert_called_once_with(1)
