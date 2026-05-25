import streamlit as st
from job_analyzer.bootstrap import create_services
from job_analyzer.ui.pages.dashboard import render_dashboard

st.set_page_config(page_title="Job Analyzer", layout="wide")

@st.cache_resource
def get_services():
    """
    Initializes and caches services to avoid re-creating
    objects on every Streamlit rerun.
    """
    return create_services()

sync_service, job_service = get_services()

render_dashboard(sync_service, job_service)
