from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class MlTrainingRun(Base):
    """ML training run model."""

    __tablename__ = 'ml_training_runs'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    training_run_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    ml_dataset_run_id: Mapped[int | None] = mapped_column(
        ForeignKey('ml_dataset_runs.id'),
        nullable=True,
    )
    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id'),
        nullable=False,
    )
    model_type: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    target_name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    is_success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    train_row_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    test_row_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    metric_mae: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    metric_rmse: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    metric_r2: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    model_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    report_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
