from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class CategoricalFeature(Base):
    """Categorical feature model."""

    __tablename__ = 'categorical_features'
    __table_args__ = (
        UniqueConstraint(
            'feature_run_id',
            'client_id',
            'company_id',
            'vacancy_id',
            'date_day',
            name='uq_categorical_features_feature_run_snapshot',
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
