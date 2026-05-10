import random
import time

from loguru import logger

from clients.api_client import ArbeitnowClient
from config import MIN_SLEEP_BETWEEN_REQUESTS, MAX_SLEEP_BETWEEN_REQUESTS
from database.file_repository import CsvRepository
from models.job_dto import JobDTO


class SyncService:

    def __init__(self, client: ArbeitnowClient, repository: CsvRepository):
        self.client = client
        self.repository = repository

    def _sync_jobs_form_page(self, page_number: int = 1):
        response = self.client.get_jobs_from_page(page_number)

        job_list = response['data']
        job_list_dto = [JobDTO(**job) for job in job_list]
        self.repository.save_jobs(job_list_dto)
        return response['links']['next']

    def __waiting(self):
        delay = random.uniform(MIN_SLEEP_BETWEEN_REQUESTS, MAX_SLEEP_BETWEEN_REQUESTS)
        logger.debug(f"Waiting {delay:.2f} seconds...'")
        time.sleep(delay)

    def sync_jobs_form_all_pages(self):
        page_number = 1
        while True:
            self.__waiting()
            has_next_page = self._sync_jobs_form_page(page_number)
            if not has_next_page:
                logger.success("All jobs have been added to the file")
                break
            page_number += 1
