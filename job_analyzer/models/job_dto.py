import hashlib

from pydantic import BaseModel, computed_field


class JobDTO(BaseModel):
    slug: str
    company_name: str
    title: str
    description: str
    remote: bool
    url: str
    tags: list[str]
    job_types: list[str]
    location: str
    created_at: str
    location: str
    created_at: int

    @computed_field
    @property
    def hash_id(self) -> str:
        raw_key = f"{self.slug}|{self.company_name}|{self.location}".lower().strip()
        return hashlib.md5(raw_key.encode()).hexdigest()