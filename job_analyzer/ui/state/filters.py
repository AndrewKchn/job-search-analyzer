import streamlit as st

def init_filters():
    if "filters" not in st.session_state:
        st.session_state.filters = {
            "location": None,
            "remote_only": False,
            "company": None,
            "keyword": ""
        }


def get_filters():
    init_filters()
    return st.session_state.filters


def update_filter(key, value):
    init_filters()
    st.session_state.filters[key] = value