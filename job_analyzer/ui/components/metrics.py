import streamlit as st

def render_metrics(df):
    total = len(df)
    remote = df[df["remote"] == True].shape[0]
    ratio = remote / total * 100 if total else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Jobs", total)
    c2.metric("Remote Jobs", remote)
    c3.metric("Remote %", f"{ratio:.1f}%")