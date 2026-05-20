import pandas as pd
from loguru import logger

from job_analyzer.infrastructure.repository.job_repository import JobRepo


class JobService:
    def __init__(self, repository: JobRepo):
        self.repository = repository

    def get_dataframe(self):
        logger.info("Attempting to fetch jobs for DataFrame conversion")
        job_list = self.repository.get_all_jobs()
        data = [job.model_dump() for job in job_list]
        df = pd.DataFrame(data)
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], unit='s')
        logger.info(f"Successfully created DataFrame with {len(df)} rows")
        return df
