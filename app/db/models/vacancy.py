from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Vacancy(Base):
    """Store actual vacancy state.
    Args:
        """
    __tablename__ = 'vacancies'

    vacancy_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id'),
        nullable=False,
    )
    company_id: Mapped[int] = mapped_column(
        ForeignKey('companies.id'),
        nullable=False,
    )
    vacancy_title: Mapped[str] = mapped_column(String(255), nullable=False)
    vacancy_description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    employment_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    profile: Mapped[str] = mapped_column(String(255), nullable=False)
    publication_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    region: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    salary_from: Mapped[int | None] = mapped_column(Integer, nullable=True)
    salary_to: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tariff: Mapped[str | None] = mapped_column(String(255), nullable=True)
    work_experience: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    work_schedule: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    standard: Mapped[int] = mapped_column(Integer, nullable=False)
    standard_plus: Mapped[int] = mapped_column(Integer, nullable=False)
    premium: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
