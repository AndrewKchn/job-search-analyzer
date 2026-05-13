import pytest

from src.clients.api_client import ArbeitnowClient
from config import ARBEITNOW_API_URL


@pytest.fixture
def arbeitnow_mock_response():
    return {
        "data": [
            {
                "slug": "it-support-engineer-munich-based-447760",
                "company_name": "Bragi",
                "title": "IT Support Engineer - Munich Based",
                "description": "Bragi was founded in 2013 and launched the world's first Truly Wireless Earphones in 2015",
                "remote": False,
                "url": "https://www.arbeitnow.com/jobs/companies/bragi/it-support-engineer-munich-based-447760",
                "tags": [
                    "Helpdesk"
                ],
                "job_types": [
                    "professional / experienced"
                ],
                "location": "Munich",
                "created_at": 1778252427
            }
        ]
    }


def test_fetch_page_arbeitnow_success(requests_mock, arbeitnow_mock_response):
    # Arrange
    client = ArbeitnowClient(ARBEITNOW_API_URL)
    adapter = requests_mock.get(ARBEITNOW_API_URL, json=arbeitnow_mock_response, status_code=200)

    # Act
    jobs = client.get_jobs_from_page(page_number=1)

    # Assert
    assert adapter.called
    assert adapter.call_count == 1
    assert len(jobs) == 1
    assert jobs['data'][0]['title'] == "IT Support Engineer - Munich Based"
    assert jobs['data'][0]['company_name'] == "Bragi"
    assert jobs['data'][0]['remote'] is False
