import logging
import sys
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

from job_analyzer.core.log_handler import InterceptHandler

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    ARBEITNOW_API_URL: str = "https://www.arbeitnow.com/api/job-board-api"

    DATA_DIR: Path = Path("data")
    DATA_CSV_FILE: str = "jobs_local_storage.csv"

    UPDATE_PAGES_LIMIT: int = 100
    MIN_SLEEP_BETWEEN_REQUESTS: int = 1
    MAX_SLEEP_BETWEEN_REQUESTS: int = 3

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )

    @property
    def DATABASE_PATH(self) -> Path:
        return self.DATA_DIR / self.DATA_CSV_FILE

    def setup_logger(self):
        logger.remove()

        logger.add(
            sink=sys.stdout,
            level=self.LOG_LEVEL,
            colorize=True,
            format=(
                "<green>{time:HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            ),
        )

        # logging.basicConfig(
        #     handlers=[InterceptHandler()],
        #     level=0,
        #     force=True)

        logger.info("Logging setup complete: Loguru + Standard Logging Bridge")


settings = Settings()
