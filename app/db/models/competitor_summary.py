from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class CompetitorSummary(Base):
    """Competitor summary model."""

    __tablename__ = 'competitor_summaries'
    __table_args__ = (
        UniqueConstraint(
            'analytics_run_id',
            name='uq_competitor_summaries_analytics_run_id',
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    analytics_run_id: Mapped[int] = mapped_column(
        ForeignKey('analytics_runs.id'),
        nullable=False,
    )
    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id'),
        nullable=False,
    )
    competitor_company_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    competitor_snapshot_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    competitor_vacancy_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    competitor_total_callbacks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    competitor_avg_callbacks: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    competitor_median_callbacks: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    competitor_mode_city: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    competitor_mode_region: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    competitor_mode_profile: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    competitor_mode_tariff: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    competitor_mode_work_schedule: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    competitor_mode_work_experience: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    competitor_mode_employment_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    competitor_median_salary_from: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    competitor_median_salary_to: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    competitor_salary_specified_share: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    competitor_salary_missing_share: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
