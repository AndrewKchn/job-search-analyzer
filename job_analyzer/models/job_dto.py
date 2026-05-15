import hashlib

from pydantic import BaseModel, Field


class JobDTO(BaseModel):
    hash_id: str = Field(default=None)
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

    def fill_hash_id(self):
        raw_key = f"{self.title}|{self.company_name}|{self.location}".lower().strip()
        self.hash_id = hashlib.md5(raw_key.encode()).hexdigest()
