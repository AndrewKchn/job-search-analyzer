import requests
from loguru import logger


class ArbeitnowClient:
    def __init__(self, url: str):
        self.url = url

    def get_jobs_from_page(self, page_number: int = 1) -> list[dict]:
        logger.info(f"GET: {self.url} page:{page_number}")
        response = requests.get(self.url, params={'page': page_number})
        logger.debug(f"{response.status_code}")

        return response.json()
