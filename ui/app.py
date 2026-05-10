import streamlit as st

from clients.api_client import ArbeitnowClient
from config import ARBEITNOW_API_URL, DATABASE_PATH, UPDATE_PAGES_LIMIT
from database.file_repository import CsvRepository
from services.job_service import JobService
from services.sync_service import SyncService

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Job Search Analyzer",
    page_icon="🔍",
    layout="wide"
)


# --- DEPENDENCY INJECTION (Service Initialization) ---
@st.cache_resource
def get_services():
    """
    Initializes and caches services to avoid re-creating
    objects on every Streamlit rerun.
    """
    repo = CsvRepository(DATABASE_PATH)
    client = ArbeitnowClient(ARBEITNOW_API_URL)

    sync_serv = SyncService(client, repo, pages_limit=UPDATE_PAGES_LIMIT)
    job_serv = JobService(repo)

    return sync_serv, job_serv


sync_service, job_service = get_services()

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.markdown("---")

    st.subheader("Data Management")
    if st.button("🔄 Fetch Latest Jobs", use_container_width=True):
        with st.spinner("Fetching latest jobs from Arbeitnow..."):
            # Execute the sync logic
            new_jobs_count = sync_service.sync_jobs_form_all_pages()

            if new_jobs_count > 0:
                st.success(f"Sync complete! Added {new_jobs_count} new records.")
            else:
                st.info("No new jobs found. Database is up to date.")

            # Clear data cache so the UI reflects changes immediately
            st.cache_data.clear()

    st.markdown("---")
    st.write("**Project Info:**")
    st.caption("This tool analyzes job market trends by fetching data from the Arbeitnow API.")

# --- MAIN CONTENT ---
st.title("📊 Job Market Analytics")

# Fetch data for visualization via JobService
jobs_df = job_service.get_dataframe()

if jobs_df is None or jobs_df.empty:
    st.warning("The database is currently empty. Please use the 'Fetch Latest Jobs' button in the sidebar.")
else:
    # 1. TOP METRICS
    total_jobs = len(jobs_df)
    remote_jobs = jobs_df[jobs_df['remote'] == True].shape[0]
    remote_percentage = (remote_jobs / total_jobs) * 100 if total_jobs > 0 else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Vacancies", total_jobs)
    m2.metric("Remote Roles", remote_jobs)
    m3.metric("Remote Ratio", f"{remote_percentage:.1f}%")

    st.markdown("---")

    # 2. VISUALIZATION TABS
    tab_charts, tab_data = st.tabs(["📈 Market Insights", "📋 Raw Data"])

    with tab_charts:
        left_col, right_col = st.columns(2)

        with left_col:
            st.subheader("Top Locations")
            # Pandas magic: count occurrences and pick top 10
            location_stats = jobs_df['location'].value_counts().head(10)
            st.bar_chart(location_stats)

        with right_col:
            st.subheader("Remote vs On-site Distribution")
            # Simple toggle for visualization
            remote_counts = jobs_df['remote'].map({True: 'Remote', False: 'On-site'}).value_counts()
            st.bar_chart(remote_counts)

    with tab_data:
        st.subheader("Stored Vacancies")
        # Searchable and sortable dataframe
        st.dataframe(
            jobs_df[['title', 'company_name', 'location', 'remote', 'tags', 'created_at']],
            use_container_width=True,
            hide_index=True
        )

# --- FOOTER ---
st.divider()
st.caption("© 2026 Job Analyzer Project | Built for ReDI School Final Project")
st.caption("Data provided by [Arbeitnow](https://www.arbeitnow.com/)")