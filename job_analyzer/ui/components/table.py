import streamlit as st

def render_table(df):
    st.subheader("Jobs")

    st.dataframe(
        df[["title", "company_name", "location", "remote", "created_at"]]
    )