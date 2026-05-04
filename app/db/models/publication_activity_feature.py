from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class PublicationActivityFeature(Base):
    """Publication activity feature model."""

    __tablename__ = 'publication_activity_features'
    __table_args__ = (
        UniqueConstraint(
            'feature_run_id',
            'client_id',
            'company_id',
            'vacancy_id',
            'date_day',
            name='uq_publication_activity_features_feature_run_snapshot',
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
    publication_activity_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    days_since_last_publication_activity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
