from functools import wraps

import streamlit as st

from job_analyzer.core.exceptions.exceptions import RepositoryError, APIConnectionError


def handle_ui_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except APIConnectionError:
            st.warning("⚠️ External service is temporarily unavailable. Please try later.")
            st.button("🔄 Refresh data", on_click=st.rerun)

        except RepositoryError:
            st.warning("Database is temporarily unavailable. Please try later.")
            st.button("🔄 Refresh data", on_click=st.rerun)

        except Exception:
            st.warning("Unexpected Application is temporarily unavailable. Please try later.")
            st.button("🔄 Refresh data", on_click=st.rerun)

    return wrapper
