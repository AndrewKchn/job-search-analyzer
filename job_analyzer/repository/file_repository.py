import ast
import csv
import os
from pathlib import Path

from loguru import logger

from job_analyzer.models.job_dto import JobDTO


class CsvRepository:

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.headers = list(JobDTO.model_fields.keys())
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        logger.debug(f"Ensure the file '{str(self.file_path)}' exists")
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not os.path.isfile(self.file_path):
            logger.debug(f"Created file: {str(self.file_path)}")
            with open(self.file_path, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()

    def get_all_jobs(self) -> list[JobDTO]:
        logger.debug(f"Getting all jobs from the file '{self.file_path}'")
        result = []
        with open(self.file_path, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['tags'] = ast.literal_eval(row['tags'])
                row['job_types'] = ast.literal_eval(row['job_types'])
                dto = JobDTO(**row)
                result.append(dto)
        logger.debug(f"Returning [{len(result)}] entries from the file '{self.file_path}'")
        return result

    def save_unique_jobs(self, vacancies: list[JobDTO]):
        logger.debug(f"Saving unique jobs to the file '{self.file_path}'")
        existing_jobs = self.get_all_jobs()
        existing_jobs_hash_id = set([j.hash_id for j in existing_jobs])
        unique_jobs_count = 0
        for v in vacancies:
            v.fill_hash_id()
        with open(self.file_path, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            for v in vacancies:
                if v.hash_id not in existing_jobs_hash_id:
                    writer.writerow(v.model_dump())
                    unique_jobs_count += 1
        logger.success(f"Added [{unique_jobs_count}] entries to the file '{self.file_path}'")
        return unique_jobs_count
