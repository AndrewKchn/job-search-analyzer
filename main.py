from job_analyzer.core.config import settings
from job_analyzer.infrastructure.clients.arbeitnow_client import ArbeitnowClient
from job_analyzer.infrastructure.repository.sql_lite.sqlite_repository import SQLiteRepository
from job_analyzer.services.sync_service import SyncService

repo = SQLiteRepository(settings.sqlite_path)


repo.get_all_jobs()

client = ArbeitnowClient(settings.ARBEITNOW_API_URL)
sync_serv = SyncService(client, repo, pages_limit=settings.UPDATE_PAGES_LIMIT)

page = sync_serv._sync_jobs_from_page(1)
print(page)


