import streamlit as st

from job_analyzer.ui.components.charts import render_charts
from job_analyzer.ui.components.footer import render_footer
from job_analyzer.ui.components.metrics import render_metrics
from job_analyzer.ui.components.project_info import render_project_info
from job_analyzer.ui.components.sidebar import render_sidebar
from job_analyzer.ui.components.table import render_table
from job_analyzer.ui.pages.analytics import apply_filters
from job_analyzer.ui.state.filters import get_filters


def render_dashboard(sync_service, job_service):

    df = job_service.get_dataframe()

    render_sidebar(sync_service, df)

    filters = get_filters()
    df = apply_filters(df, filters)

    st.title("📊 Job Market Dashboard")

    render_metrics(df)

    st.divider()

    render_charts(df)

    render_table(df)

    st.divider()
    render_project_info()

    render_footer()