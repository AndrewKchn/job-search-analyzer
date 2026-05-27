import requests
from loguru import logger

from job_analyzer.core.exceptions.exceptions import APIConnectionError


class ArbeitnowClient:
    def __init__(self, url: str):
        self.url = url

    def get_jobs_from_page(self, page_number: int = 1) -> dict:
        logger.info(f"GET: {self.url}?page={page_number}")
        try:
            response = requests.get(self.url, params={'page': page_number}, timeout=5)
            logger.debug(f"{response.status_code}")
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Arbeitnow API failed: {e}")
            raise APIConnectionError("Failed to fetch jobs from API") from e
        return response.json()