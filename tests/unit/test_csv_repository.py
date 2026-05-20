import pytest

from job_analyzer.infrastructure.repository.csv_file.file_repository import CsvRepository
from job_analyzer.models.job_dto import JobDTO


@pytest.fixture
def repo(tmp_path):
    db_file = tmp_path / "test.db"

    return CsvRepository(db_file)


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


def test_save_unique_jobs(repo, fake_job):
    # Act
    inserted = repo.save_unique_jobs([fake_job])

    # Assert
    assert inserted == 1


def test_duplicate_jobs_are_ignored(repo, fake_job):
    # Act
    first_insert = repo.save_unique_jobs([fake_job])
    second_insert = repo.save_unique_jobs([fake_job])

    # Assert
    assert first_insert == 1
    assert second_insert == 0


def test_get_all_jobs(repo, fake_job):
    # Act
    repo.save_unique_jobs([fake_job])
    jobs = repo.get_all_jobs()

    # Assert
    assert len(jobs) == 1
    assert jobs[0].title == "Python Developer"
