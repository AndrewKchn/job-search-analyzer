import requests
from loguru import logger

from models.job_dto import JobDTO


class Fetcher:
    def __init__(self, url: str):
        self.url = url

    def fetch_page(self, page_number: int = 0):
        logger.info(f"GET: {self.url}")
        response = requests.get(self.url, params={'page': page_number})
        logger.debug(f"{response.status_code}: {response.text}")

        job_list = response.json()['data']
        return [JobDTO(**job) for job in job_list]
