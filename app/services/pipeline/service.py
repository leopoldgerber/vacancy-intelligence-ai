import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.pipeline.run_pipeline_1 import run_pipeline_1


async def execute_pipeline_1(
    session: AsyncSession,
    data: pd.DataFrame,
    source_name: str,
) -> dict[str, object]:
    """Execute pipeline 1.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset.
        source_name (str): Source dataset name."""
    pipeline_result = await run_pipeline_1(
        session=session,
        data=data,
        source_name=source_name,
    )
    return pipeline_result
