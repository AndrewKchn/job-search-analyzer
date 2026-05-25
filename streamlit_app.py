import streamlit as st

from job_analyzer.bootstrap import create_services
from job_analyzer.ui.components.footer import render_footer
from job_analyzer.ui.components.sidebar import render_sidebar
from job_analyzer.ui.pages.dashboard import render_dashboard, render_empty_dashboard

st.set_page_config(
    page_title="Job Search Analyzer",
    page_icon="🔍",
    layout="wide"
)


@st.cache_resource
def get_services():
    """
    Initializes and caches services to avoid re-creating
    objects on every Streamlit rerun.
    """
    return create_services()


sync_service, job_service = get_services()


def render_app(sync_service, job_service):
    # LOAD DATA
    df = job_service.get_dataframe()

    # SIDEBAR ALWAYS EXISTS
    render_sidebar(sync_service, df)

    # HEADER
    st.title("📊 Job Market Analytics")

    # EMPTY DATABASE
    if df is None or df.empty:
        render_empty_dashboard()
        render_footer()
        return

    # MAIN DASHBOARD
    render_dashboard(df)

    # FOOTER
    render_footer()


render_app(sync_service, job_service)
