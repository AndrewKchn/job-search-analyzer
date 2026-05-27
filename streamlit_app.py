import streamlit as st

from job_analyzer.bootstrap import create_services
from job_analyzer.core.decorators.error_handler import handle_ui_errors
from job_analyzer.ui.components.footer import render_footer
from job_analyzer.ui.components.sidebar import render_sidebar
from job_analyzer.ui.pages.analytics import apply_filters
from job_analyzer.ui.pages.dashboard import render_dashboard, render_empty_dashboard
from job_analyzer.ui.state.filters import get_filters

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


@st.cache_data(ttl=60)
def load_df():
    return job_service.get_dataframe()

@handle_ui_errors
def render_app(sync_service):
    # LOAD DATA
    df = load_df()

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
    filters = get_filters()
    df_filtered = apply_filters(df, filters)
    render_dashboard(df_filtered)

    # FOOTER
    render_footer()


render_app(sync_service)
