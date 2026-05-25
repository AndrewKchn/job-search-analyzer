from datetime import datetime

from loguru import logger
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from job_analyzer.infrastructure.mappers.job_mapper import JobMapper
from job_analyzer.core.exceptions.exceptions import RepositoryError
from job_analyzer.core.interfaces.job_repository import JobRepo
from job_analyzer.infrastructure.database.models.models import JobORM


class BaseSQLRepository(JobRepo):
    insert_function = None

    def get_all_jobs(self):
        with self.session_factory() as session:
            job_list_orm = session.query(JobORM).all()
            job_list_dto = [JobMapper.orm_to_dto(job) for job in job_list_orm]
            logger.debug(f"Fetched {len(job_list_dto)} jobs")
            return job_list_dto

    def get_existing_job_ids(self, hashes: list[str]) -> set[str]:
        with self.session_factory() as session:
            stmt = select(JobORM.hash_id).where(JobORM.hash_id.in_(hashes))
            result = session.execute(stmt).scalars().all()
            return set(result)

    def insert_jobs(self, jobs, sync_time):
        if not jobs:
            return 0

        jobs_rows = [JobMapper.dto_to_row(job, sync_time) for job in jobs]

        with self.session_factory() as session:
            try:
                stmt = self.insert_function(JobORM).values(jobs_rows)
                stmt = stmt.on_conflict_do_nothing(index_elements=["hash_id"])
                result = session.execute(stmt)
                session.commit()

                inserted = result.rowcount or 0
                logger.success(f"Inserted {inserted} new jobs")
                return inserted
            except SQLAlchemyError as e:
                session.rollback()
                raise RepositoryError("Failed to insert jobs") from e

    def touch_jobs(self, hashes: list[str], ts: datetime) -> int:
        if not hashes:
            return 0

        with self.session_factory() as session:
            stmt = (
                update(JobORM)
                .where(JobORM.hash_id.in_(hashes))
                .values(
                    last_seen=ts,
                    is_active=True
                )
            )

            result = session.execute(stmt)
            session.commit()
            logger.success(f"Marked {result.rowcount} jobs as touched")
            return result.rowcount or 0

    def mark_jobs_inactive(self, sync_ts: int) -> int:
        with self.session_factory() as session:
            stmt = (
                update(JobORM)
                .where(JobORM.last_seen < sync_ts,
                       JobORM.is_active == True)
                .values(is_active=False)
            )

            result = session.execute(stmt)
            session.commit()
            logger.success(f"Marked {result.rowcount} jobs as inactive")
            return result.rowcount or 0
