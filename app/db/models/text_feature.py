from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class TextFeature(Base):
    """Text feature model."""

    __tablename__ = 'text_features'
    __table_args__ = (
        UniqueConstraint(
            'feature_run_id',
            'client_id',
            'company_id',
            'vacancy_id',
            'date_day',
            name='uq_text_features_feature_run_snapshot',
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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
