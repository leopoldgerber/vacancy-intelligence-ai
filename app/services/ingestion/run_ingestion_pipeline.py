import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import VacancyIngestionError
from app.core.exceptions import VacancySnapshotIngestionError
from app.services.ingestion.companies.service import upsert_companies
from app.services.ingestion.vacancies.service import upsert_vacancies
from app.services.ingestion.vacancy_snapshots.service import (
    insert_vacancy_snapshots,
)


async def run_ingestion_pipeline(
    session: AsyncSession,
    data: pd.DataFrame,
) -> dict[str, int]:
    """Run full ingestion pipeline.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset."""
    company_map = await upsert_companies(
        session=session,
        data=data,
    )

    try:
        vacancy_id_map = await upsert_vacancies(
            session=session,
            data=data,
            company_map=company_map,
        )
    except Exception as exc:
        raise VacancyIngestionError() from exc

    try:
        created_snapshots = await insert_vacancy_snapshots(
            session=session,
            data=data,
            company_map=company_map,
        )
    except Exception as exc:
        raise VacancySnapshotIngestionError() from exc

    await session.commit()

    ingestion_result = {
        'company_count': len(company_map),
        'vacancy_count': len(vacancy_id_map),
        'snapshot_count': len(created_snapshots),
    }
    return ingestion_result
