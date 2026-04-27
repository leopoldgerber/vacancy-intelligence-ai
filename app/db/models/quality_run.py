from datetime import datetime


from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class QualityRun(Base):
    """Store quality run metadata.
    Args:
        """
    __tablename__ = 'quality_runs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quality_name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    warning_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    report_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    quality_issue = relationship(
        'QualityIssue',
        back_populates='quality_run',
        uselist=False,
        cascade='all, delete-orphan',
    )
