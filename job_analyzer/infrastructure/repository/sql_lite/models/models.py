from sqlalchemy import String, Integer, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

from job_analyzer.infrastructure.repository.sql_lite.models.base import Base


class JobORM(Base):
    __tablename__ = "jobs"

    hash_id: Mapped[str] = mapped_column(String, primary_key=True)

    slug: Mapped[str] = mapped_column(String)

    company_name: Mapped[str] = mapped_column(String)

    title: Mapped[str] = mapped_column(String)

    description: Mapped[str] = mapped_column(Text)

    remote: Mapped[bool] = mapped_column(Boolean)

    url: Mapped[str] = mapped_column(String)

    tags: Mapped[str] = mapped_column(Text)

    job_types: Mapped[str] = mapped_column(Text)

    location: Mapped[str] = mapped_column(String)

    created_at: Mapped[int] = mapped_column(Integer)