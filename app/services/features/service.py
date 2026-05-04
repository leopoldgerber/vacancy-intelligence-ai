from datetime import datetime

from app.db.session import SessionLocal
from app.services.features.run_publication_activity_features_pipeline import (
    run_publication_activity_features_pipeline,
)
from app.services.features.run_salary_features_pipeline import (
    run_salary_features_pipeline,
)


async def run_salary_features(
    client_id: int,
    date_from: datetime,
    date_to: datetime,
) -> dict[str, int | str | bool]:
    """Run salary feature engineering service.
    Args:
        client_id (int): Client identifier.
        date_from (datetime): Feature period start.
        date_to (datetime): Feature period end.
    """
    async with SessionLocal() as session:
        async with session.begin():
            feature_result = await run_salary_features_pipeline(
                session=session,
                client_id=client_id,
                date_from=date_from,
                date_to=date_to,
            )

    return feature_result


async def run_publication_activity_features(
    client_id: int,
    date_from: datetime,
    date_to: datetime,
) -> dict[str, int | str | bool]:
    """Run publication activity feature engineering service.
    Args:
        client_id (int): Client identifier.
        date_from (datetime): Feature period start.
        date_to (datetime): Feature period end.
    """
    async with SessionLocal() as session:
        async with session.begin():
            feature_result = (
                await run_publication_activity_features_pipeline(
                    session=session,
                    client_id=client_id,
                    date_from=date_from,
                    date_to=date_to,
                )
            )

    return feature_result
