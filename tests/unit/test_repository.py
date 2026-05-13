from src.models.job_dto import JobDTO
from src.repository.file_repository import CsvRepository


def test_save_jobs(tmp_path):
    # Arrange
    file_path = tmp_path / "jobs.csv"

    repo = CsvRepository(str(file_path))

    jobs = [
        JobDTO(
            slug="python-dev",
            company_name="Google",
            title="Python Dev",
            description="Test",
            remote=True,
            url="https://example.com",
            tags=["python"],
            job_types=["full-time"],
            location="Berlin",
            created_at=123456,
        )
    ]
    # Act

    repo.save_unique_jobs(jobs)

    # Assert
    assert file_path.exists()
    content = file_path.read_text()
    assert "Google" in content
    assert "Python Dev" in content