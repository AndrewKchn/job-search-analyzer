import streamlit as st

from job_analyzer.services.trends_service import TrendsService
from job_analyzer.ui.components.charts import render_charts
from job_analyzer.ui.components.metrics import render_metrics
from job_analyzer.ui.components.table import render_table
from job_analyzer.ui.components.trends import render_trends


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

    # TRENDS
    trends_service = TrendsService(df)
    tab1, tab2, tab3 = st.tabs(["Daily", "Weekly", "Monthly"])

    with tab1:
        render_trends(trends_service.daily_trends(), "Daily Trends")

    with tab2:
        render_trends(trends_service.weekly_trends(), "Weekly Trends")

    with tab3:
        render_trends(trends_service.monthly_trends(), "Monthly Trends")


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