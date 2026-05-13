from unittest.mock import MagicMock, patch

import pytest

from config import UPDATE_PAGES_LIMIT
from models.job_dto import JobDTO
from services.sync_service import SyncService


@pytest.fixture
def fake_job_data():
    return {
        "data": [
            {
                "slug": "werkstudentin",
                "company_name": "Kiwimo-Product GmbH",
                "title": "Python Developer",
                "description": "Unsere Marke WhyWords unterstützt Unternehmer:innen",
                "remote": True,
                "url": "https://www.arbeitnow.com/jobs/companies/kiwimo-product-gmbh/",
                "tags": [
                    "Remote",
                    "Marketing and Communication"
                ],
                "job_types": [
                    "Working student",
                    "hilfstätigkeit / student"
                ],
                "location": "Cologne",
                "created_at": 1778437858
            }
        ],
        "links": {"next": "https://api.arbeitnow.com/jobs?page=2"}
    }


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def service(mock_client, mock_repo):
    return SyncService(client=mock_client, repository=mock_repo, pages_limit=2)


def test_sync_jobs_from_page_success(mock_client, mock_repo, fake_job_data):
    # Arrange
    mock_client.get_jobs_from_page.return_value = fake_job_data
    service = SyncService(client=mock_client, repository=mock_repo, pages_limit=UPDATE_PAGES_LIMIT)

    # Act
    service._sync_jobs_from_page(page_number=1)

    # Assert
    mock_client.get_jobs_from_page.assert_called_once_with(1)
    mock_repo.save_unique_jobs.assert_called_once()
    passed_jobs = mock_repo.save_unique_jobs.call_args[0][0]
    assert passed_jobs[0].title == "Python Developer"
    assert isinstance(passed_jobs[0], JobDTO)


@patch('time.sleep', return_value=None)
def test_sync_jobs_from_all_pages_stops_at_limit(mock_sleep, service, mock_client, mock_repo):
    # Arrange
    mock_client.get_jobs_from_page.side_effect = [
        {'data': [], 'links': {'next': 'url2'}},
        {'data': [], 'links': {'next': 'url3'}},
    ]
    mock_repo.save_unique_jobs.return_value = 5

    # Act
    total = service.sync_jobs_from_all_pages()

    # Assert
    assert total == 10
    assert mock_client.get_jobs_from_page.call_count == 2


@patch('time.sleep', return_value=None)
def test_sync_jobs_from_all_pages_stops_when_no_next(mock_sleep, service, mock_client, mock_repo):
    # Arrange
    mock_client.get_jobs_from_page.return_value = {
        'data': [],
        'links': {'next': None}
    }
    mock_repo.save_unique_jobs.return_value = 3

    # Act
    total = service.sync_jobs_from_all_pages()

    # Assert
    assert total == 3
    assert mock_client.get_jobs_from_page.call_count == 1
