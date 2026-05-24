from loguru import logger

from job_analyzer.core.config import settings
from job_analyzer.infrastructure.clients.arbeitnow_client import ArbeitnowClient
from job_analyzer.infrastructure.database.repositories.postgres_repository import PostgresRepository
from job_analyzer.services.analytics_service import JobAnalyticsService
from job_analyzer.services.lifecycle_service import JobLifecycleService
from job_analyzer.services.sync_service import SyncService


def create_services():
    logger.debug("Initializing Services...")

    repo = PostgresRepository(settings.POSTGRES_DB_URL)

    client = ArbeitnowClient(settings.ARBEITNOW_API_URL)
    lifecycle_service = JobLifecycleService(repo)

    sync_service = SyncService(client, lifecycle_service)
    job_analytics_service = JobAnalyticsService(repo)

    logger.debug("Services initialized!")
    return sync_service, job_analytics_service
