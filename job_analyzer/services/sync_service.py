import random
import time

from loguru import logger
from pydantic import ValidationError

from job_analyzer.core.config import settings
from job_analyzer.infrastructure.clients.arbeitnow_client import ArbeitnowClient
from job_analyzer.models.job_dto import JobDTO
from job_analyzer.services.lifecycle_service import JobLifecycleService


class SyncService:

    def __init__(self, client: ArbeitnowClient, job_lifecycle_service: JobLifecycleService):
        self.client = client
        self.job_lifecycle_service = job_lifecycle_service

    def _apply_rate_limit_delay(self):
        """Introduces a random delay to prevent hitting API rate limits (HTTP 429)."""
        delay = random.uniform(settings.MIN_SLEEP_BETWEEN_REQUESTS, settings.MAX_SLEEP_BETWEEN_REQUESTS)
        logger.debug(f"Waiting {delay:.2f} seconds...'")
        time.sleep(delay)

    def _normalize_job(self, job: dict) -> dict:
        job = job.copy()

        if isinstance(job.get("job_types"), dict):
            job["job_types"] = list(job["job_types"].values())

        if isinstance(job.get("tags"), dict):
            job["tags"] = list(job["tags"].values())

        return job

    def sync_jobs_from_all_pages(self):
        logger.info(f"Syncing jobs form all pages...")
        jobs_dict = self._receive_all_jobs()
        job_list_dto = []
        invalid_jobs = []

        for i, job in enumerate(jobs_dict):
            try:
                job = self._normalize_job(job)
                job_list_dto.append(JobDTO(**job))
            except ValidationError as e:
                logger.warning("Skipping invalid job {}: {}", i, e, )
                invalid_jobs.append(job)

        # job_list_dto = [JobDTO(**job) for job in jobs_dict]  # TODO: need to fix the validation
        logger.info(
            "Received {} jobs: {} valid, {} invalid",
            len(jobs_dict),
            len(job_list_dto),
            len(invalid_jobs),
        )
        return self.job_lifecycle_service.sync_jobs(job_list_dto)

    def _receive_all_jobs(self) -> list[dict]:
        logger.info(f"Receiving all jobs...")
        all_jobs = []
        page_number = 1
        while True:
            response_json = self.client.get_jobs_from_page(page_number)  # TODO: need try-except
            all_jobs.extend(response_json["data"])
            if not response_json['links']['next'] or page_number == settings.UPDATE_PAGES_LIMIT:
                return all_jobs
            else:
                page_number += 1
                self._apply_rate_limit_delay()
