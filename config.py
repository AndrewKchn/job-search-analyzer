from loguru import logger

# 1.
ARBEITNOW_API_URL = "https://www.arbeitnow.com/api/job-board-api"

# 2.
DATABASE_PATH = "jobs_local_storage.csv"

# 3.
# MAX_PAGES = 2
REQUEST_TIMEOUT = 10
MIN_SLEEP_BETWEEN_REQUESTS = 2
MAX_SLEEP_BETWEEN_REQUESTS = 5

# 4.
LOG_FILE = "logs_app.log"


def setup_logging():
    """Setup Loguru"""
    logger.remove()

    # Console log
    logger.add(
        sink=lambda msg: print(msg, end=""),
        colorize=True,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="DEBUG"
    )

    # File log
    logger.add(LOG_FILE, rotation="10 MB", level="INFO")


# Init logger
setup_logging()
