from clients.fetcher import Fetcher

fetcher = Fetcher("https://www.arbeitnow.com/api/job-board-api")

jobs = fetcher.fetch_page()

print(jobs)