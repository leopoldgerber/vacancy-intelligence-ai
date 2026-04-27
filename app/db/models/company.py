from datetime import datetime


from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Company(Base):
    """Store company reference data.
    Args:
        """
    __tablename__ = 'companies'
    __table_args__ = (
        UniqueConstraint(
            'client_id',
            'name',
            name='uq_companies_client_id_name',
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(
        ForeignKey('clients.id'),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
