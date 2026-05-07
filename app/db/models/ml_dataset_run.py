from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class MlDatasetRun(Base):
    """ML dataset run model."""

    __tablename__ = 'ml_dataset_runs'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    dataset_run_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id'),
        nullable=False,
    )
    date_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
    )
    date_to: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
    )

    salary_feature_run_id: Mapped[int | None] = mapped_column(
        ForeignKey('feature_runs.id'),
        nullable=True,
    )
    publication_activity_feature_run_id: Mapped[int | None] = mapped_column(
        ForeignKey('feature_runs.id'),
        nullable=True,
    )
    text_feature_run_id: Mapped[int | None] = mapped_column(
        ForeignKey('feature_runs.id'),
        nullable=True,
    )
    time_feature_run_id: Mapped[int | None] = mapped_column(
        ForeignKey('feature_runs.id'),
        nullable=True,
    )
    categorical_feature_run_id: Mapped[int | None] = mapped_column(
        ForeignKey('feature_runs.id'),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    is_success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    row_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    report_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
