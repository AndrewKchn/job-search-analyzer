import csv
import os

from models.job_dto import JobDTO
from loguru import logger

class CsvRepository:

    def __init__(self, filename: str):
        self.filename = filename
        self.fieldnames = list(JobDTO.model_fields.keys())

    def save_jobs(self, vacancies: list[JobDTO]):
        try:
            file_exists = os.path.isfile(self.filename)
            if not file_exists:
                os.makedirs("local_storage", exist_ok=True)

            with open(self.filename, mode='a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)

                if not file_exists:
                    writer.writeheader()

                for v in vacancies:
                    writer.writerow(v.model_dump())

            logger.success(f"Added [{len(vacancies)}] entries to the file '{self.filename}'")
        except Exception as e:
            logger.error(f"Error writing CSV: {e}")