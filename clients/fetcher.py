import requests

from models.job_dto import JobDTO


class Fetcher:
    def __init__(self, url: str):
        self.url = url

    def fetch_page(self, page_number: int = 0):
        return requests.get(self.url, params={'page': page_number}).json()


