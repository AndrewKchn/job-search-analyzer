import streamlit as st

def get_filters():
    location = st.session_state.get("location")

    return {
        "location": None if location == "All" else location,
        "remote_only": st.session_state.get("remote_only", False),
        "keyword": st.session_state.get("keyword", ""),
    }
