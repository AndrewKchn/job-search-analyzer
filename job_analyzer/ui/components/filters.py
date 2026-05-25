import streamlit as st


def render_filters(df):
    st.subheader("Filters")

    locations = sorted(
        df["location"].dropna().unique().tolist()
    )

    st.selectbox(
        "Location",
        options=["All"] + locations,
        key="location"
    )

    st.toggle(
        "Remote only",
        key="remote_only"
    )

    st.text_input(
        "Keyword search",
        placeholder="Python, Backend...",
        key="keyword"
    )