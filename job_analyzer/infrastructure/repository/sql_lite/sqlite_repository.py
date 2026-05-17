import json
from pathlib import Path
from sqlite3 import IntegrityError

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from job_analyzer.infrastructure.repository.sql_lite.models.base import Base
from job_analyzer.infrastructure.repository.sql_lite.models.models import JobORM
from job_analyzer.models.job_dto import JobDTO
from sqlalchemy.dialects.sqlite import insert

def convert_to(vacancies: list[JobDTO]):
    rows =[]
    for job in vacancies:
        rows.append({
            "hash_id": job.hash_id,
            "slug": job.slug,
            "company_name": job.company_name,
            "title": job.title,
            "description": job.description,
            "remote": job.remote,
            "url": job.url,
            "tags": json.dumps(job.tags),
            "job_types": json.dumps(job.job_types),
            "location": job.location,
            "created_at": job.created_at,
        })
    return rows

class SQLiteRepository:

    def __init__(self, db_path: Path):
        logger.info(f"Initializing SQLiteRepository with DB: {db_path}")
        self.db_path = db_path
        self.engine = create_engine(
            f"sqlite:///{db_path}",
            echo=False
        )
        self.session_factory = sessionmaker(bind=self.engine)
        self._initialize_database()

    def _initialize_database(self):

        if self.db_path.exists():
            logger.info("Database already exists")
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

    def get_all_jobs(self) -> list[JobDTO]:
        logger.info("Fetching all jobs from database")

        with self.session_factory() as session:
            jobs = session.query(JobORM).all()

            result = []

            for job in jobs:
                dto = JobDTO(
                    hash_id=job.hash_id,
                    slug=job.slug,
                    company_name=job.company_name,
                    title=job.title,
                    description=job.description,
                    remote=job.remote,
                    url=job.url,
                    tags=json.loads(job.tags),
                    job_types=json.loads(job.job_types),
                    location=job.location,
                    created_at=job.created_at
                )

                result.append(dto)

            logger.info(f"Fetched {len(result)} jobs")

            return result

    def save_unique_jobs(self, vacancies: list[JobDTO]) -> int:
        logger.info(f"Attempting to save {len(vacancies)} jobs")
        orm = convert_to(vacancies)

        with self.session_factory() as session:
            try:
                stmt = insert(JobORM).values(orm)
                stmt = stmt.on_conflict_do_nothing(index_elements=["hash_id"])
                result = session.execute(stmt)
                session.commit()

                inserted = result.rowcount if result.rowcount is not None else 0
                logger.success(f"Inserted {inserted} new jobs")
                return inserted
            except SQLAlchemyError as e:
                session.rollback()
                logger.exception("DB error during bulk insert")
                return 0



    def _save_unique_jobs(self, vacancies: list[JobDTO]) -> int:
        """
        Fast bulk insert with deduplication at DB level.
        """

        if not vacancies:
            logger.info("No vacancies to save")
            return 0

        session = self.session_factory()

        try:
            logger.info(f"Saving {len(vacancies)} jobs (bulk insert)")

            # 1. prepare data for bulk insert
            rows = []
            for job in vacancies:
                rows.append({
                    "hash_id": job.hash_id,
                    "slug": job.slug,
                    "company_name": job.company_name,
                    "title": job.title,
                    "description": job.description,
                    "remote": job.remote,
                    "url": job.url,
                    "tags": json.dumps(job.tags),
                    "job_types": json.dumps(job.job_types),
                    "location": job.location,
                    "created_at": job.created_at,
                })

            # 2. SQLite upsert (ignore duplicates)
            stmt = insert(JobORM).values(rows)

            stmt = stmt.on_conflict_do_nothing(
                index_elements=["hash_id"]
            )

            result = session.execute(stmt)
            session.commit()

            inserted = result.rowcount if result.rowcount is not None else 0

            logger.success(f"Inserted {inserted} new jobs")
            return inserted

        except SQLAlchemyError as e:
            session.rollback()
            logger.exception("DB error during bulk insert")
            return 0

        finally:
            session.close()