from unittest.mock import MagicMock

import pandas as pd
import pytest

from services.job_service import JobService


@pytest.fixture
def mock_repository():
    return MagicMock()


@pytest.fixture
def mock_job_service(mock_repository):
    return JobService(repository=mock_repository)


def test_get_dataframe_success(mock_job_service, mock_repository):
    # Arrange
    job1 = MagicMock()
    job1.model_dump.return_value = {'company_name': "Bragi", 'title': 'Python Dev', 'created_at': 1715580000}
    job2 = MagicMock()
    job2.model_dump.return_value = {'company_name': "Bragi", 'title': 'Data Scientist', 'created_at': 1715583600}

    mock_repository.get_all_jobs.return_value = [job1, job2]

    # Act
    df = mock_job_service.get_dataframe()

    # Assert
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ['company_name', 'title', 'created_at']
    assert isinstance(df['created_at'][0], pd.Timestamp)
    mock_repository.get_all_jobs.assert_called_once()


def test_get_dataframe_empty_repository(mock_job_service, mock_repository):
    # Arrange
    mock_repository.get_all_jobs.return_value = []

    # Act
    df = mock_job_service.get_dataframe()

    # Assert
    assert len(df) == 0
    assert isinstance(df, pd.DataFrame)
