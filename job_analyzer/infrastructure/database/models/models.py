from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

from job_analyzer.infrastructure.database.models.base import Base


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
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
