import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.company import Company
from app.services.ingestion.companies.persistence import (
    create_company,
    save_companies,
)
from app.services.ingestion.companies.repositories import (
    get_companies_by_client_ids,
)


def build_company_pairs(data: pd.DataFrame) -> list[tuple[int, str]]:
    """Build unique client and company pairs.
    Args:
        data (pd.DataFrame): Input dataset."""
    company_data = data[['client_id', 'company_name']].drop_duplicates()

    company_pairs = [
        (int(row.client_id), str(row.company_name))
        for row in company_data.itertuples(index=False)
    ]
    return company_pairs


def build_company_map(
    companies: list[Company],
) -> dict[tuple[int, str], int]:
    """Build company identifier map.
    Args:
        companies (list[Company]): Company model instances."""
    company_map = {
        (company.client_id, company.name): company.id
        for company in companies
    }
    return company_map


async def upsert_companies(
    session: AsyncSession,
    data: pd.DataFrame,
) -> dict[tuple[int, str], int]:
    """Upsert companies from dataset into database.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset."""
    company_pairs = build_company_pairs(data=data)
    client_ids = list({client_id for client_id, _ in company_pairs})

    existing_companies = await get_companies_by_client_ids(
        session=session,
        client_ids=client_ids,
    )
    existing_company_map = build_company_map(companies=existing_companies)

    companies_to_create: list[Company] = []

    for client_id, company_name in company_pairs:
        company_key = (client_id, company_name)

        if company_key in existing_company_map:
            continue

        company = create_company(
            client_id=client_id,
            name=company_name,
        )
        companies_to_create.append(company)

    created_companies = await save_companies(
        session=session,
        companies=companies_to_create,
    )

    all_companies = existing_companies + created_companies
    company_map = build_company_map(companies=all_companies)

    return company_map
