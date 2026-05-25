import streamlit as st

from job_analyzer.ui.components.filters import render_filters


def render_sync_section(sync_serv):
    st.subheader("Data Management")
    if st.button("🔄 Fetch Latest Jobs", width='stretch'):
        with st.spinner("Fetching latest jobs from Arbeitnow..."):
            # Execute the sync logic
            sync_result = sync_serv.sync_jobs_from_all_pages()
            st.session_state["sync_result"] = sync_result

            # Clear data cache so the UI reflects changes immediately
            st.cache_data.clear()
        st.rerun()

    if "sync_result" in st.session_state:
        sync_result = st.session_state.pop("sync_result")

        st.success(
            f"""
            Sync complete!\n\n
            ✅ New jobs: {sync_result.new_jobs} \n
            🔄 Existing jobs refreshed: {sync_result.updated_jobs} \n
            ❌ Inactivated jobs: {sync_result.inactive_jobs}
            """
        )


def render_sidebar(sync_service, df):
    with st.sidebar:
        # HEADER
        st.title("⚙️ Control Panel")
        st.caption("Job Market Analytics Dashboard")
        st.divider()

        # EMPTY DATABASE
        if df is None or df.empty:
            st.info("No jobs loaded yet.")
            render_sync_section(sync_service)
            return

        # FILTERS
        render_filters(df)
        st.divider()
        render_sync_section(sync_service)
