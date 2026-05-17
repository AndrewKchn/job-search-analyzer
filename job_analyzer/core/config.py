import sys
from pathlib import Path

from loguru import logger
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    ARBEITNOW_API_URL: str = "https://www.arbeitnow.com/api/job-board-api"

    DATA_DIR: Path = Path("data")
    CSV_FILE: str = "jobs_local_storage.csv"
    SQL_LITE_DB: str = "jobs_local_storage.db"

    UPDATE_PAGES_LIMIT: int = 100
    MIN_SLEEP_BETWEEN_REQUESTS: int = 1
    MAX_SLEEP_BETWEEN_REQUESTS: int = 3

    LOG_LEVEL: str = "INFO"

    @computed_field
    @property
    def csv_file_path(self) -> Path:
        return self.DATA_DIR / self.CSV_FILE

    @computed_field
    @property
    def sqlite_path(self) -> Path:
        return self.DATA_DIR / self.SQL_LITE_DB

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )

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

        logger.info("Logging setup complete: Loguru + Standard Logging Bridge")


settings = Settings()
