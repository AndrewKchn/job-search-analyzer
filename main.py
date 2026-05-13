from clients.api_client import ArbeitnowClient
from config import ARBEITNOW_API_URL, DATABASE_PATH, UPDATE_PAGES_LIMIT
from repository.file_repository import CsvRepository
from services.sync_service import SyncService

client = ArbeitnowClient(ARBEITNOW_API_URL)
repo = CsvRepository(DATABASE_PATH)

service = SyncService(client=client, repository=repo, pages_limit=UPDATE_PAGES_LIMIT)

service.sync_jobs_from_all_pages()