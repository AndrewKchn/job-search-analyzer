from pathlib import Path

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool.impl import StaticPool

from job_analyzer.infrastructure.database.repositories.base_sql_repository import BaseSQLRepository
from job_analyzer.infrastructure.database.models.base import Base


class SQLiteRepository(BaseSQLRepository):
    insert_function = staticmethod(insert)

    def __init__(self, db_path: Path):
        logger.debug(f"Initializing SQLiteRepository with DB: {db_path}")
        self.db_path = db_path
        self.engine = create_engine(
            f"sqlite:///{db_path}",
            echo=False,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )
        self.session_factory = sessionmaker(bind=self.engine)
        self._initialize_database()

    def _initialize_database(self):

        if self.db_path.exists():
            logger.debug("Database already exists")
        else:
            logger.warning("Database not found. Creating new database")
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created directory: {str(self.db_path.parent)}")

        Base.metadata.create_all(bind=self.engine)
        logger.info(
            f"Registered tables: "
            f"{Base.metadata.tables.keys()}"
        )
        logger.success("Database initialized successfully")