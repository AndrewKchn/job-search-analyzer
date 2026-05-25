import streamlit as st


def render_trends(trends, title: str):
    st.subheader(title)
    st.line_chart(trends)