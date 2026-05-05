from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class TimeFeature(Base):
    """Time feature model."""

    __tablename__ = 'time_features'
    __table_args__ = (
        UniqueConstraint(
            'feature_run_id',
            'client_id',
            'company_id',
            'vacancy_id',
            'date_day',
            name='uq_time_features_feature_run_snapshot',
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
