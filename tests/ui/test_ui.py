from unittest.mock import Mock

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from job_analyzer.core.config import BASE_DIR


@pytest.fixture
def app_path():
    return BASE_DIR / "streamlit_app.py"

@pytest.fixture(autouse=True)
def clear_streamlit_cache():
    import streamlit as st

    st.cache_resource.clear()
    st.cache_data.clear()

    yield

    st.cache_resource.clear()
    st.cache_data.clear()

@pytest.fixture
def mock_services(monkeypatch):
    def make_services(df=None, mock_sync_jobs_from_all_pages=None):
        job_service = Mock()
        job_service.get_dataframe.return_value = df if df is not None else pd.DataFrame()

        sync_service = Mock()

        if mock_sync_jobs_from_all_pages is not None:
            sync_service.sync_jobs_from_all_pages.side_effect = mock_sync_jobs_from_all_pages

        monkeypatch.setattr(
            "job_analyzer.bootstrap.create_services",
            lambda: (sync_service, job_service)
        )

        return job_service, sync_service

    return make_services


def test_app_initial_load(app_path, mock_services):
    # Arrange
    mock_services(df=pd.DataFrame())

    # Act
    at = AppTest.from_file(app_path).run(timeout=5)

    # Assert
    assert not at.exception
    assert at.title[0].value == "📊 Job Market Analytics"


def test_app_with_empty_data(app_path, mock_services):
    # Arrange
    mock_services(df=pd.DataFrame())

    # Act
    at = AppTest.from_file(app_path).run()

    # Assert
    assert not at.exception
    assert "The database is currently empty" in at.warning[0].value


def test_sidebar_fetch_button(app_path, mock_services):
    # Arrange
    mock_sync_jobs_from_all_pages = Mock(return_value=5)
    mock_services(mock_sync_jobs_from_all_pages=mock_sync_jobs_from_all_pages)

    # Act
    at = AppTest.from_file(app_path).run()
    at.sidebar.button[0].click().run()

    # Assert
    assert not at.exception
    assert "Sync complete! Added 5 new records." in at.success[0].value
    mock_sync_jobs_from_all_pages.assert_called_once()
