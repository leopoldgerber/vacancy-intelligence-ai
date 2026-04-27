import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.ingestion.run_ingestion_pipeline import (
    run_ingestion_pipeline,
)


async def ingest_data(
    session: AsyncSession,
    data: pd.DataFrame,
) -> dict[str, int]:
    """Run ingestion service.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset."""
    ingestion_result = await run_ingestion_pipeline(
        session=session,
        data=data,
    )
    return ingestion_result
