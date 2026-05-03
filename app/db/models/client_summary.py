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


class ClientSummary(Base):
    """Client summary model."""

    __tablename__ = 'client_summaries'
    __table_args__ = (
        UniqueConstraint(
            'analytics_run_id',
            name='uq_client_summaries_analytics_run_id',
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
    client_company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    client_snapshot_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    client_vacancy_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    client_total_callbacks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    client_avg_callbacks: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    client_median_callbacks: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    client_mode_city: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    client_mode_region: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    client_mode_profile: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    client_mode_tariff: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    client_mode_work_schedule: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    client_mode_work_experience: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    client_mode_employment_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    client_median_salary_from: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    client_median_salary_to: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    client_salary_specified_share: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    client_salary_missing_share: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
