import pytest
from pydantic import ValidationError

from src.models.job_dto import JobDTO


def test_job_dto_valid():
    dto = JobDTO(
        slug="python-dev",
        company_name="Google",
        title="Python Developer",
        description="Test",
        remote=True,
        url="https://test.com",
        tags=["python"],
        job_types=["full-time"],
        location="Berlin",
        created_at=123456,
    )

    assert dto.company_name == "Google"


def test_invalid_job_dto_raises_validation_error():
    with pytest.raises(ValidationError):
        JobDTO(
            slug=123,  # Must be a string
            company_name="Google",
            title="Python Developer",
            description="Test",
            remote=True,
            url="https://test.com",
            tags=["python"],
            job_types=["full-time"],
            location="Berlin",
            created_at=123456,
        )