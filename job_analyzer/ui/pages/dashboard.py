import streamlit as st

from job_analyzer.ui.components.charts import render_charts
from job_analyzer.ui.components.metrics import render_metrics
from job_analyzer.ui.components.table import render_table
from job_analyzer.ui.pages.analytics import apply_filters
from job_analyzer.ui.state.filters import get_filters


def render_dashboard(df):



    # EMPTY FILTER RESULT
    if df.empty:
        st.warning("No jobs match current filters.")
        st.info("Try changing filters in the sidebar 👈")
        return

    # DASHBOARD SUMMARY
    st.caption(f"Showing {len(df)} jobs")

    # METRICS
    render_metrics(df)
    st.divider()

    # CHARTS
    render_charts(df)
    st.divider()

    # TABLE
    render_table(df)


def render_empty_dashboard():
    st.info("👋 Welcome to Job Search Analyzer")

    st.markdown(
        """
        Your database is currently empty.

        To get started:

        1. Open the sidebar 👈
        2. Click **🔄 Fetch Latest Jobs**
        3. Wait for synchronization to finish
        4. Explore market analytics and trends

        ---

        Features available after sync:
        - 📈 Market analytics
        - 🌍 Location insights
        - 🏠 Remote work statistics
        - 🏢 Company analytics
        - 🔍 Advanced filtering
        """
    )