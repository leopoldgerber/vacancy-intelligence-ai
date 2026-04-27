import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CompanyMappingError
from app.db.models.vacancy_snapshot import VacancySnapshot
from app.services.ingestion.vacancies.service import parse_datetime_value
from app.services.ingestion.vacancies.service import parse_nullable_integer
from app.services.ingestion.vacancies.service import parse_nullable_string
from app.services.ingestion.vacancy_snapshots.persistence import (
    create_vacancy_snapshot,
)
from app.services.ingestion.vacancy_snapshots.repositories import (
    get_existing_snapshot_keys,
)


async def insert_vacancy_snapshots(
    session: AsyncSession,
    data: pd.DataFrame,
    company_map: dict[tuple[int, str], int],
) -> list[VacancySnapshot]:
    """Insert vacancy snapshots from dataset into database.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset.
        company_map (dict[tuple[int, str], int]): Company identifier map."""
    client_ids = [
        int(value) for value in data['client_id'].unique().tolist()
    ]
    vacancy_ids = [
        int(value) for value in data['vacancy_id'].unique().tolist()
    ]

    company_ids = list(
        {
            int(company_map[(int(row.client_id), str(row.company_name))])
            for row in data.itertuples(index=False)
            if (int(row.client_id), str(row.company_name)) in company_map
        }
    )

    existing_snapshot_keys = await get_existing_snapshot_keys(
        session=session,
        client_ids=client_ids,
        company_ids=company_ids,
        vacancy_ids=vacancy_ids,
    )

    snapshots_to_create: list[VacancySnapshot] = []

    for row in data.itertuples(index=False):
        client_id = int(row.client_id)
        company_name = str(row.company_name)
        company_key = (client_id, company_name)

        if company_key not in company_map:
            raise CompanyMappingError(
                detail=(
                    'Failed to resolve company mapping for '
                    f'client_id={client_id}, company_name={company_name}.'
                ),
            )

        company_id = company_map[company_key]
        vacancy_id = int(row.vacancy_id)
        date_day = parse_datetime_value(row.date_day)

        snapshot_key = (
            client_id,
            company_id,
            vacancy_id,
            date_day,
        )

        if snapshot_key in existing_snapshot_keys:
            continue

        vacancy_snapshot = create_vacancy_snapshot(
            client_id=client_id,
            company_id=company_id,
            vacancy_id=vacancy_id,
            date_day=date_day,
            publication_date=parse_datetime_value(row.publication_date),
            vacancy_title=str(row.vacancy_title),
            vacancy_description=str(row.vacancy_description),
            employment_type=parse_nullable_string(row.employment_type),
            profile=str(row.profile),
            region=str(row.region),
            city=str(row.city),
            salary_from=parse_nullable_integer(row.salary_from),
            salary_to=parse_nullable_integer(row.salary_to),
            tariff=parse_nullable_string(row.tariff),
            work_experience=parse_nullable_string(row.work_experience),
            work_schedule=parse_nullable_string(row.work_schedule),
            standard=int(row.standard),
            standard_plus=int(row.standard_plus),
            premium=int(row.premium),
            callbacks=int(row.callbacks),
        )
        snapshots_to_create.append(vacancy_snapshot)
        existing_snapshot_keys.add(snapshot_key)

    if snapshots_to_create:
        session.add_all(snapshots_to_create)
        await session.flush()

    return snapshots_to_create
