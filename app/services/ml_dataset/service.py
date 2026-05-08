from datetime import datetime

from app.db.session import SessionLocal
from app.services.ml_dataset.run_ml_dataset_pipeline import (
    run_ml_dataset_pipeline,
)


async def run_ml_dataset(
    client_id: int,
    date_from: datetime,
    date_to: datetime,
) -> dict[str, int | str | bool]:
    """Run ML dataset service.
    Args:
        client_id (int): Client identifier.
        date_from (datetime): Dataset period start.
        date_to (datetime): Dataset period end.
    """
    async with SessionLocal() as session:
        async with session.begin():
            dataset_result = await run_ml_dataset_pipeline(
                session=session,
                client_id=client_id,
                date_from=date_from,
                date_to=date_to,
            )

    return dataset_result
