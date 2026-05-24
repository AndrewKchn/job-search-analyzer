import json

from job_analyzer.infrastructure.database.models.models import JobORM
from job_analyzer.models.job_dto import JobDTO


class JobMapper:

    @staticmethod
    def dto_to_orm_dict(job: JobDTO) -> dict:
        ...

    @staticmethod
    def orm_to_dto(job: JobORM) -> JobDTO:
        return JobDTO(
            slug=job.slug,
            company_name=job.company_name,
            title=job.title,
            description=job.description,
            remote=job.remote,
            url=job.url,
            tags=json.loads(job.tags),
            job_types=json.loads(job.job_types),
            location=job.location,
            created_at=job.created_at,
            first_seen_at=job.first_seen,
            last_seen_at=job.last_seen,
            is_active=job.is_active
        )

    @staticmethod
    def dto_to_row(job: JobDTO, sync_time: int) -> dict:
        return {
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

            # lifecycle
            "first_seen": sync_time,
            "last_seen": sync_time,
            "is_active": True,
        }
