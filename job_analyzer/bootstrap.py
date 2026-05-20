from loguru import logger

from job_analyzer.core.config import settings
from job_analyzer.infrastructure.clients.arbeitnow_client import ArbeitnowClient
from job_analyzer.infrastructure.repository.sql_lite.sqlite_repository import SQLiteRepository
from job_analyzer.services.job_service import JobService
from job_analyzer.services.sync_service import SyncService


def create_services():
    logger.debug("Initializing Services...")
    repo = SQLiteRepository(settings.sqlite_path)
    client = ArbeitnowClient(settings.ARBEITNOW_API_URL)

    sync_service = SyncService(client, repo, pages_limit=settings.UPDATE_PAGES_LIMIT)
    job_service = JobService(repo)

    logger.debug("Services initialized!")
    return sync_service, job_service
