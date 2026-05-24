import pytest

from job_analyzer.infrastructure.database.models.models import JobORM
from job_analyzer.infrastructure.database.repositories.sqlite_repository import SQLiteRepository
from job_analyzer.models.job_dto import JobDTO


@pytest.fixture
def repo(tmp_path):
    db_file = tmp_path / "test.db"

    return SQLiteRepository(db_file)


@pytest.fixture
def fake_job():
    return JobDTO(
        slug="python-dev",
        company_name="Google",
        title="Python Developer",
        description="Backend work",
        remote=True,
        url="https://example.com",
        tags=["python", "backend"],
        job_types=["full-time"],
        location="Berlin",
        created_at=123456
    )


def test_insert_jobs(repo, fake_job):
    # Arrange
    inserted = repo.insert_jobs([fake_job], sync_time=100)

    # Act
    jobs = repo.get_all_jobs()

    # Assert
    assert inserted == 1
    assert len(jobs) == 1

    job = jobs[0]
    assert job.title == "Python Developer"

def test_insert_duplicate_jobs(repo, fake_job):
    # Act
    first = repo.insert_jobs([fake_job], sync_time=100)
    second = repo.insert_jobs([fake_job], sync_time=100)

    # Assert
    assert first == 1
    assert second == 0

def test_get_existing_hashes(repo, fake_job):
    # Arrange
    repo.insert_jobs([fake_job], sync_time=100)

    # Act
    hashes = repo.get_existing_job_ids([fake_job.hash_id])

    # Assert
    assert fake_job.hash_id in hashes

def test_touch_jobs_updates_last_seen(repo, fake_job):
    repo.insert_jobs([fake_job], sync_time=100)

    updated = repo.touch_jobs(
        [fake_job.hash_id],
        ts=200
    )

    assert updated == 1

    with repo.session_factory() as session:
        orm_job = session.query(JobORM).first()

        assert orm_job.last_seen == 200
        assert orm_job.is_active is True