import ast
import csv
from pathlib import Path

from loguru import logger

from job_analyzer.infrastructure.repository.job_repository import JobRepo
from job_analyzer.models.job_dto import JobDTO


class CsvRepository(JobRepo):

    def __init__(self, csv_file_path: Path):
        logger.debug("Initializing CsvRepository")
        self.csv_file_path = csv_file_path
        self.headers = list(JobDTO.model_computed_fields.keys())
        self.headers.extend(list(JobDTO.model_fields.keys()))
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        logger.debug(f"Ensure the file '{str(self.csv_file_path)}' exists")
        self.csv_file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.csv_file_path.exists():
            logger.debug(f"Created file: {str(self.csv_file_path)}")
            with open(self.csv_file_path, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()

    def get_all_jobs(self) -> list[JobDTO]:
        logger.debug(f"Getting all jobs from the file '{self.csv_file_path}'")
        result = []
        with open(self.csv_file_path, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['tags'] = ast.literal_eval(row['tags'])
                row['job_types'] = ast.literal_eval(row['job_types'])
                dto = JobDTO(**row)
                result.append(dto)
        logger.debug(f"Returning [{len(result)}] entries from the file '{self.csv_file_path}'")
        return result

    def save_unique_jobs(self, vacancies: list[JobDTO]):
        logger.debug(f"Saving unique jobs to the file '{self.csv_file_path}'")
        existing_jobs = self.get_all_jobs()
        existing_jobs_hash_id = set([j.hash_id for j in existing_jobs])
        unique_jobs_count = 0
        with open(self.csv_file_path, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            for v in vacancies:
                if v.hash_id not in existing_jobs_hash_id:
                    writer.writerow(v.model_dump())
                    unique_jobs_count += 1
        logger.success(f"Added [{unique_jobs_count}] entries to the file '{self.csv_file_path}'")
        return unique_jobs_count
