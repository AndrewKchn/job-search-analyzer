import streamlit as st

from job_analyzer.ui.state.filters import update_filter


def render_sidebar(sync_service, df):

    with st.sidebar:
        st.title("⚙️ Filters")

        location = st.selectbox(
            "Location",
            options=["All"] + sorted(df["location"].dropna().unique().tolist())
        )

        remote_only = st.toggle("Remote only")

        keyword = st.text_input("Keyword search")

        update_filter("location", None if location == "All" else location)
        update_filter("remote_only", remote_only)
        update_filter("keyword", keyword)

        st.markdown("---")

        st.subheader("Data Management")
        if st.button("🔄 Fetch Latest Jobs", width='stretch'):
            with st.spinner("Fetching latest jobs from Arbeitnow..."):
                sync_result = sync_service.sync_jobs_from_all_pages()

                st.success(
                    f"""
                       Sync complete!\n\n

                       ✅ New jobs: {sync_result.new_jobs} \n
                       🔄 Existing jobs refreshed: {sync_result.updated_jobs} \n
                       ❌ Inactivated jobs: {sync_result.inactive_jobs}
                       """
                )

                # Clear data cache so the UI reflects changes immediately
                st.cache_data.clear()