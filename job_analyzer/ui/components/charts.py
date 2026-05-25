import streamlit as st

def render_charts(df):

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Top Locations")
        st.bar_chart(df["location"].value_counts().head(10))

    with c2:
        st.subheader("Remote vs Onsite")
        st.bar_chart(df["remote"].map({True:"Remote", False:"Onsite"}).value_counts())