from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker

from job_analyzer.infrastructure.database.models.base import Base
from job_analyzer.infrastructure.database.repositories.base_sql_repository import BaseSQLRepository


class PostgresRepository(BaseSQLRepository):
    insert_function = staticmethod(insert)

    def __init__(self, db_url: str):
        logger.debug("Initializing Postgres repository (Supabase connection)")

        self.engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False
        )
        self.session_factory = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
