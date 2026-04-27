from datetime import datetime

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CompanyMappingError
from app.db.models.vacancy import Vacancy
from app.services.ingestion.vacancies.persistence import (
    create_vacancy,
    update_vacancy,
)
from app.services.ingestion.vacancies.repositories import (
    get_vacancies_by_ids,
)


def parse_datetime_value(value: object) -> datetime:
    """Parse datetime value.
    Args:
        value (object): Raw datetime value."""
    parsed_value = pd.to_datetime(value)
    datetime_value = parsed_value.to_pydatetime()
    return datetime_value


def parse_nullable_string(value: object) -> str | None:
    """Parse nullable string value.
    Args:
        value (object): Raw string value."""
    if pd.isna(value):
        return None

    string_value = str(value)

    if string_value.strip() == '':
        return None

    return string_value


def parse_nullable_integer(value: object) -> int | None:
    """Parse nullable integer value.
    Args:
        value (object): Raw integer value."""
    if pd.isna(value):
        return None

    integer_value = int(value)
    return integer_value


def build_vacancy_map(
    vacancies: list[Vacancy],
) -> dict[int, Vacancy]:
    """Build vacancy model map by vacancy identifier.
    Args:
        vacancies (list[Vacancy]): Vacancy model instances."""
    vacancy_map = {
        vacancy.vacancy_id: vacancy
        for vacancy in vacancies
    }
    return vacancy_map


def build_vacancy_id_map(
    vacancies: list[Vacancy],
) -> dict[int, int]:
    """Build vacancy identifier map.
    Args:
        vacancies (list[Vacancy]): Vacancy model instances."""
    vacancy_id_map = {
        vacancy.vacancy_id: vacancy.vacancy_id
        for vacancy in vacancies
    }
    return vacancy_id_map


async def upsert_vacancies(
    session: AsyncSession,
    data: pd.DataFrame,
    company_map: dict[tuple[int, str], int],
) -> dict[int, int]:
    """Upsert vacancies from dataset into database.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset.
        company_map (dict[tuple[int, str], int]): Company identifier map."""
    vacancy_ids = [
        int(value) for value in data['vacancy_id'].unique().tolist()
    ]

    existing_vacancies = await get_vacancies_by_ids(
        session=session,
        vacancy_ids=vacancy_ids,
    )
    existing_vacancy_map = build_vacancy_map(vacancies=existing_vacancies)

    created_vacancies: list[Vacancy] = []

    latest_rows = (
        data.sort_values(by=['vacancy_id', 'date_day'])
        .drop_duplicates(subset=['vacancy_id'], keep='last')
    )

    for row in latest_rows.itertuples(index=False):
        vacancy_id = int(row.vacancy_id)
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

        vacancy_title = str(row.vacancy_title)
        vacancy_description = str(row.vacancy_description)
        employment_type = parse_nullable_string(row.employment_type)
        profile = str(row.profile)
        publication_date = parse_datetime_value(row.publication_date)
        region = str(row.region)
        city = str(row.city)
        salary_from = parse_nullable_integer(row.salary_from)
        salary_to = parse_nullable_integer(row.salary_to)
        tariff = parse_nullable_string(row.tariff)
        work_experience = parse_nullable_string(row.work_experience)
        work_schedule = parse_nullable_string(row.work_schedule)
        standard = int(row.standard)
        standard_plus = int(row.standard_plus)
        premium = int(row.premium)

        existing_vacancy = existing_vacancy_map.get(vacancy_id)

        if existing_vacancy is None:
            vacancy = create_vacancy(
                vacancy_id=vacancy_id,
                client_id=client_id,
                company_id=company_id,
                vacancy_title=vacancy_title,
                vacancy_description=vacancy_description,
                employment_type=employment_type,
                profile=profile,
                publication_date=publication_date,
                region=region,
                city=city,
                salary_from=salary_from,
                salary_to=salary_to,
                tariff=tariff,
                work_experience=work_experience,
                work_schedule=work_schedule,
                standard=standard,
                standard_plus=standard_plus,
                premium=premium,
            )
            session.add(vacancy)
            created_vacancies.append(vacancy)
            continue

        update_vacancy(
            vacancy=existing_vacancy,
            client_id=client_id,
            company_id=company_id,
            vacancy_title=vacancy_title,
            vacancy_description=vacancy_description,
            employment_type=employment_type,
            profile=profile,
            publication_date=publication_date,
            region=region,
            city=city,
            salary_from=salary_from,
            salary_to=salary_to,
            tariff=tariff,
            work_experience=work_experience,
            work_schedule=work_schedule,
            standard=standard,
            standard_plus=standard_plus,
            premium=premium,
        )

    await session.flush()

    all_vacancies = existing_vacancies + created_vacancies
    vacancy_id_map = build_vacancy_id_map(vacancies=all_vacancies)

    return vacancy_id_map
