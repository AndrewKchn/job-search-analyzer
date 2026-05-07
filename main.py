from clients.fetcher import Fetcher
from database.file_repository import CsvRepository

fetcher = Fetcher("https://www.arbeitnow.com/api/job-board-api")

jobs = fetcher.fetch_page()

repository = CsvRepository("local_storage/jobs.csv")
repository.save_jobs(jobs)
