import streamlit as st

from job_analyzer.services.trends_service import TrendsService


def render_trends(trends, title: str):
    st.subheader(title)
    st.line_chart(trends)


def render_trends_section(df):
    trends_service = TrendsService(df)

    tab1, tab2, tab3 = st.tabs(["Daily", "Weekly", "Monthly"])

    with tab1:
        render_trends(trends_service.daily_trends(), "Daily Trends")

    with tab2:
        render_trends(trends_service.weekly_trends(), "Weekly Trends")

    with tab3:
        render_trends(trends_service.monthly_trends(), "Monthly Trends")
