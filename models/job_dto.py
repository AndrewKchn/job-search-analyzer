from typing import List

from pydantic import BaseModel


class JobDTO(BaseModel):
    slug: str
    company_name: str
    title: str
    description: str
    remote: bool
    url: str
    tags: List[str]
    job_types: List[str]
    location: str
    created_at: str
    location: str
    created_at: int
