from pathlib import Path
from unittest.mock import patch

import pytest
from streamlit.testing.v1 import AppTest

from job_analyzer.core.config import BASE_DIR


@pytest.fixture
def app_path():
    return BASE_DIR / "streamlit_app.py"


def test_app_initial_load(app_path):
    at = AppTest.from_file(app_path).run()

    assert not at.exception
    assert at.title[0].value == "📊 Job Market Analytics"


@patch('job_analyzer.services.job_service.JobService.get_dataframe')
def test_app_with_empty_data(mock_get_df, app_path):
    import pandas as pd
    mock_get_df.return_value = pd.DataFrame()

    at = AppTest.from_file(app_path).run()

    assert "The database is currently empty" in at.warning[0].value


@patch('job_analyzer.services.sync_service.SyncService.sync_jobs_from_all_pages')
def test_sidebar_fetch_button(mock_sync_service, app_path):
    mock_sync_service.return_value = 5

    at = AppTest.from_file(app_path).run()

    fetch_button = at.sidebar.button[0]
    fetch_button.click().run()

    assert mock_sync_service.called
    assert "Sync complete! Added 5 new records." in at.success[0].value
