import random
import time

from loguru import logger

from src.clients.api_client import ArbeitnowClient
from config import MIN_SLEEP_BETWEEN_REQUESTS, MAX_SLEEP_BETWEEN_REQUESTS
from src.repository.file_repository import CsvRepository
from src.models.job_dto import JobDTO


class SyncService:

    def __init__(self, client: ArbeitnowClient, repository: CsvRepository, pages_limit: int):
        self.client = client
        self.repository = repository
        self.pages_limit = pages_limit

    def _sync_jobs_from_page(self, page_number: int = 1):
        logger.debug(f"Syncing jobs form page {page_number}...")
        response = self.client.get_jobs_from_page(page_number)

        job_list = response['data']
        job_list_dto = [JobDTO(**job) for job in job_list]
        unique_jobs_count = self.repository.save_unique_jobs(job_list_dto)
        return response['links']['next'], unique_jobs_count

    def _waiting(self):
        delay = random.uniform(MIN_SLEEP_BETWEEN_REQUESTS, MAX_SLEEP_BETWEEN_REQUESTS)
        logger.debug(f"Waiting {delay:.2f} seconds...'")
        time.sleep(delay)

    def sync_jobs_from_all_pages(self):
        logger.info(f"Syncing jobs form all pages...")
        page_number = 1
        total_job_count = 0
        while True:
            self._waiting()
            has_next_page, unique_jobs_count = self._sync_jobs_from_page(page_number)
            total_job_count += unique_jobs_count
            if not has_next_page or page_number == self.pages_limit:
                logger.info(f"{total_job_count} jobs have been added")
                return total_job_count
            page_number += 1
