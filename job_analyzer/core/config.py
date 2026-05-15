import logging
import sys
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

from job_analyzer.core.log_handler import InterceptHandler

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    ARBEITNOW_API_URL: str
    DATABASE_PATH: str

    UPDATE_PAGES_LIMIT: int
    REQUEST_TIMEOUT: int
    MIN_SLEEP_BETWEEN_REQUESTS: int
    MAX_SLEEP_BETWEEN_REQUESTS: int

    LOG_LEVEL: str

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

        logging.basicConfig(
            handlers=[InterceptHandler()],
            level=0,
            force=True)

        logger.info("Logging setup complete: Loguru + Standard Logging Bridge")


settings = Settings()
