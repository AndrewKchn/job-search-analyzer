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

    # def get_all_jobs(self) -> list[JobDTO]:
    #     logger.debug("Fetching all jobs from database")
    #     with self.session_factory() as session:
    #         job_list_orm = session.query(JobORM).all()
    #         job_list_dto = [JobMapper.orm_to_dto(job) for job in job_list_orm]
    #         logger.debug(f"Fetched {len(job_list_dto)} jobs")
    #         return job_list_dto
    #
    # def get_existing_job_ids(self, hashes: list[str]) -> set[str]:
    #     with self.session_factory() as session:
    #         stmt = select(JobORM.hash_id).where(JobORM.hash_id.in_(hashes))
    #         result = session.execute(stmt).scalars().all()
    #
    #         return set(result)
    #
    # def insert_jobs(self, jobs: list[JobDTO], sync_time) -> int:
    #     logger.info(f"Attempting to save {len(jobs)} jobs")
    #     if not jobs:
    #         logger.debug("No jobs were saved")
    #         return 0
    #     jobs_rows = [JobMapper.dto_to_row(job, sync_time) for job in jobs]
    #
    #     with self.session_factory() as session:
    #         try:
    #             stmt = insert(JobORM).values(jobs_rows)
    #             stmt = stmt.on_conflict_do_nothing(index_elements=["hash_id"])
    #             result = session.execute(stmt)
    #             session.commit()
    #
    #             inserted = result.rowcount if result.rowcount is not None else 0
    #             logger.success(f"Inserted {inserted} new jobs")
    #             return inserted
    #         except SQLAlchemyError as e:
    #             session.rollback()
    #             logger.exception("DB error during bulk insert")
    #             raise RepositoryError("Failed to save jobs") from e
    #
    # def touch_jobs(self, hashes: list[str], ts: int) -> int:
    #     logger.info(f"Attempting to mark {len(hashes)} jobs as touched")
    #     if not hashes:
    #         logger.debug("No jobs were saved")
    #         return 0
    #
    #     with self.session_factory() as session:
    #         stmt = (
    #             update(JobORM)
    #             .where(JobORM.hash_id.in_(hashes))
    #             .values(
    #                 last_seen=ts,
    #                 is_active=True
    #             )
    #         )
    #
    #         result = session.execute(stmt)
    #         session.commit()
    #         logger.success(f"Marked {result.rowcount} jobs as touched")
    #         return result.rowcount or 0
    #
    # def mark_jobs_inactive(self, sync_ts: int) -> int:
    #     with self.session_factory() as session:
    #         stmt = (
    #             update(JobORM)
    #             .where(JobORM.last_seen < sync_ts,
    #                    JobORM.is_active == True)
    #             .values(is_active=False)
    #         )
    #
    #         result = session.execute(stmt)
    #         session.commit()
    #         logger.success(f"Marked {result.rowcount} jobs as inactive")
    #         return result.rowcount or 0
