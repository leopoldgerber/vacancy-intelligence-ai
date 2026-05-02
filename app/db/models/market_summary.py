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


class MarketSummary(Base):
    """Market summary model."""

    __tablename__ = 'market_summaries'
    __table_args__ = (
        UniqueConstraint(
            'analytics_run_id',
            name='uq_market_summaries_analytics_run_id',
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
    total_snapshot_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    total_company_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    total_vacancy_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    total_callbacks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    avg_callbacks: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    median_callbacks: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    mode_city: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    mode_region: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    mode_profile: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    mode_tariff: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    mode_work_schedule: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    mode_work_experience: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    mode_employment_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    median_salary_from: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    median_salary_to: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    salary_specified_share: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    salary_missing_share: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
