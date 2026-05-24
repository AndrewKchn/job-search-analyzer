import time

from job_analyzer.core.interfaces.job_repository import JobRepo
from job_analyzer.models.job_dto import JobDTO
from job_analyzer.models.sync_result import SyncResult


class JobLifecycleService:
    def __init__(self, repo: JobRepo):
        self.repo = repo

    def sync_jobs(self, incoming_jobs: list[JobDTO]):
        sync_time = int(time.time())
        existing_job_ids = self.repo.get_existing_job_ids([job.hash_id for job in incoming_jobs])

        new_jobs_saved = self._save_new_jobs(incoming_jobs, existing_job_ids, sync_time)
        updated_jobs = self._update_jobs_timestamps(incoming_jobs, existing_job_ids, sync_time)
        inactive_jobs = self._mark_inactive_jobs(sync_time)
        return SyncResult(
            new_jobs=new_jobs_saved,
            updated_jobs=updated_jobs,
            inactive_jobs=inactive_jobs
        )

    def _save_new_jobs(self, incoming_jobs: list[JobDTO], existing_job_ids: set, sync_time) -> int:
        new_jobs = self._detect_new_jobs_for_insert(incoming_jobs, existing_job_ids)
        return self.repo.insert_jobs(new_jobs, sync_time) if new_jobs else 0

    def _update_jobs_timestamps(self, incoming_jobs: list[JobDTO], existing_job_ids: set, sync_time):
        existing_jobs = self._detect_existing_jobs_for_update(incoming_jobs, existing_job_ids)
        return self.repo.touch_jobs(existing_jobs, sync_time)

    def _mark_inactive_jobs(self, sync_time):
        return self.repo.mark_jobs_inactive(sync_time)

    def _detect_new_jobs_for_insert(self, jobs, existing_job_ids):
        return [job for job in jobs if job.hash_id not in existing_job_ids]

    def _detect_existing_jobs_for_update(self, jobs, existing_job_ids):
        return [job.hash_id for job in jobs if job.hash_id in existing_job_ids]
