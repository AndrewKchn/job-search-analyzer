import streamlit as st


def render_table(df):
    st.subheader("Stored Vacancies")

    st.dataframe(
        df[["title", "company_name", "location", "description", "remote", "created_at"]],
        column_config={
            "title": "Title",
            "company_name": "Company",
            "location": "Location",
            "description": "Description",
            "remote": "Remote",
            "tags": "Tags",
            "created_at": "Creation Date"
        },
        hide_index=True
    )
