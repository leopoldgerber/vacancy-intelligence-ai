from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class SalaryFeature(Base):
    """Salary feature model."""

    __tablename__ = 'salary_features'
    __table_args__ = (
        UniqueConstraint(
            'feature_run_id',
            'client_id',
            'company_id',
            'vacancy_id',
            'date_day',
            name='uq_salary_features_feature_run_snapshot',
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    feature_run_id: Mapped[int] = mapped_column(
        ForeignKey('feature_runs.id'),
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
    salary_mid: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    salary_is_specified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    company_salary_median_by_city: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    market_salary_median_excl_company_by_city: Mapped[float] = (
        mapped_column(
            Float,
            nullable=False,
        )
    )
    salary_ratio_to_market_by_city: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    company_salary_median_by_profile: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    market_salary_median_excl_company_by_profile: Mapped[float] = (
        mapped_column(
            Float,
            nullable=False,
        )
    )
    salary_ratio_to_market_by_profile: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    company_salary_median_by_city_profile: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    market_salary_median_excl_company_by_city_profile: Mapped[float] = (
        mapped_column(
            Float,
            nullable=False,
        )
    )
    salary_ratio_to_market_by_city_profile: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
