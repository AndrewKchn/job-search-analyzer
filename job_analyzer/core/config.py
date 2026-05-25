import sys
from pathlib import Path

from loguru import logger
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    logger.debug('Setting up .env config')
    ENV: str = "local"
    ARBEITNOW_API_URL: str = "https://www.arbeitnow.com/api/job-board-api"

    DATA_DIR: Path = Path("data")
    SQL_LITE_DB: str = "jobs_local_storage.db"
    POSTGRES_DB_URL: str | None = None

    UPDATE_PAGES_LIMIT: int = 100
    MIN_SLEEP_BETWEEN_REQUESTS: int = 2
    MAX_SLEEP_BETWEEN_REQUESTS: int = 5

    LOG_LEVEL: str = "DEBUG"

    @computed_field
    @property
    def sqlite_path(self) -> Path:
        return self.DATA_DIR / self.SQL_LITE_DB

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )
    logger.debug('Setting up .env config done!')

    def setup_logger(self):
        logger.debug('Setting up logger')
        logger.remove()

        logger.add(
            sink=sys.stdout,
            level=self.LOG_LEVEL,
            colorize=True
        )

        logger.debug("Logging setup complete!")


settings = Settings()