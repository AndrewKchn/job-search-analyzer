from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker

from job_analyzer.infrastructure.database.repositories.base_sql_repository import BaseSQLRepository
from job_analyzer.infrastructure.database.models.base import Base


class PostgresRepository(BaseSQLRepository):
    insert_function = staticmethod(insert)

    def __init__(self, db_url: str):
        logger.debug(f"Initializing Postgres repository with {db_url}")

        self.engine = create_engine(
            db_url,
            echo=False
        )
        self.session_factory = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
