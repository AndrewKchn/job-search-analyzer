from typing import Protocol

from job_analyzer.models.job_dto import JobDTO


class JobRepo(Protocol):

    def get_all_jobs(self) -> list[JobDTO]: ...

    def save_unique_jobs(self, vacancies: list[JobDTO]) -> int: ...
