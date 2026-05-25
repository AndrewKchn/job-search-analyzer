import streamlit as st

def render_project_info():
    st.markdown("---")

    st.subheader("Project Info")

    st.caption(
        "This tool analyzes job market trends by fetching and processing real-time job data "
        "from the Arbeitnow API. It demonstrates ETL pipeline, analytics layer, and dashboard UI."
    )