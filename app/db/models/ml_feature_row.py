from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class MlFeatureRow(Base):
    """Materialized ML feature row model."""

    __tablename__ = 'ml_feature_rows'
    __table_args__ = (
        UniqueConstraint(
            'ml_dataset_run_id',
            'client_id',
            'company_id',
            'vacancy_id',
            'date_day',
            name='uq_ml_feature_rows_dataset_snapshot',
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    ml_dataset_run_id: Mapped[int] = mapped_column(
        ForeignKey('ml_dataset_runs.id'),
        nullable=False,
    )

    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id'),
        nullable=False,
    )
    company_id: Mapped[int] = mapped_column(
        ForeignKey('companies.id'),
        nullable=False,
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey('vacancies.vacancy_id'),
        nullable=False,
    )
    date_day: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
    )

    callbacks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    salary_mid: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    salary_is_specified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    salary_ratio_to_market_by_city: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    salary_ratio_to_market_by_profile: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    salary_ratio_to_market_by_city_profile: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    publication_activity_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    days_since_last_publication_activity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    title_length: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    description_length: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    title_word_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    description_word_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    has_description: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    description_is_empty: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    has_salary_mention: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    has_schedule_mention: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    has_requirements_mention: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    has_benefits_mention: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    has_call_to_action: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    publication_hour: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    publication_day_of_week: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    publication_month: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    publication_week: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    is_weekend: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    vacancy_age_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    region: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    profile: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    employment_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    work_experience: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    work_schedule: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
