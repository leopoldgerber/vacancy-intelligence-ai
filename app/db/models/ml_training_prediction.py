from datetime import date
from datetime import datetime

from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class MlTrainingPrediction(Base):
    """ML training prediction row model."""

    __tablename__ = 'ml_training_predictions'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    ml_training_run_id: Mapped[int] = mapped_column(
        ForeignKey('ml_training_runs.id'),
        nullable=False,
    )
    source_row_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id'),
        nullable=False,
    )
    company_id: Mapped[int | None] = mapped_column(
        ForeignKey('companies.id'),
        nullable=True,
    )
    vacancy_id: Mapped[int | None] = mapped_column(
        ForeignKey('vacancies.vacancy_id'),
        nullable=True,
    )
    date_day: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )
    split_name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )
    target_name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    actual_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    predicted_value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    prediction_error: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    absolute_error: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    squared_error: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
