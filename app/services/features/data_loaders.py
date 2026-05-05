from datetime import datetime

import pandas as pd
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.vacancy_snapshot import VacancySnapshot


async def load_feature_snapshot_data(
    session: AsyncSession,
    client_id: int,
    date_from: datetime,
    date_to: datetime,
) -> pd.DataFrame:
    """Load vacancy snapshots for feature engineering.
    Args:
        session (AsyncSession): Database session.
        client_id (int): Client identifier.
        date_from (datetime): Feature period start.
        date_to (datetime): Feature period end.
    """
    statement = (
        select(VacancySnapshot)
        .where(VacancySnapshot.client_id == client_id)
        .where(VacancySnapshot.date_day >= date_from)
        .where(VacancySnapshot.date_day <= date_to)
    )

    result = await session.execute(statement)
    snapshots = result.scalars().all()

    rows = [
        {
            'client_id': snapshot.client_id,
            'company_id': snapshot.company_id,
            'vacancy_id': snapshot.vacancy_id,
            'date_day': snapshot.date_day,
            'publication_date': snapshot.publication_date,
            'salary_from': snapshot.salary_from,
            'salary_to': snapshot.salary_to,
            'city': snapshot.city,
            'profile': snapshot.profile,
            'standard': snapshot.standard,
            'standard_plus': snapshot.standard_plus,
            'premium': snapshot.premium,
            'vacancy_title': snapshot.vacancy_title,
            'vacancy_description': snapshot.vacancy_description,
        }
        for snapshot in snapshots
    ]

    return pd.DataFrame(rows)
