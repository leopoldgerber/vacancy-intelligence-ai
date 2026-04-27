import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.ingestion.service import ingest_data
from app.services.pre_ingestion.service import prepare_data_for_ingestion


async def run_pipeline_1(
    session: AsyncSession,
    data: pd.DataFrame,
    source_name: str,
) -> dict[str, object]:
    """Run full pipeline 1.
    Args:
        session (AsyncSession): Async database session.
        data (pd.DataFrame): Input dataset.
        source_name (str): Source dataset name."""
    pre_ingestion_result = await prepare_data_for_ingestion(
        session=session,
        data=data,
        source_name=source_name,
    )

    if not pre_ingestion_result['should_ingest']:
        pipeline_result = {
            'status': 'failed',
            'message': 'Pre-ingestion checks failed.',
            'pre_ingestion_result': pre_ingestion_result,
            'ingestion_result': None,
        }
        return pipeline_result

    ingestion_result = await ingest_data(
        session=session,
        data=data,
    )

    pipeline_result = {
        'status': 'ok',
        'message': 'Pipeline 1 completed successfully.',
        'pre_ingestion_result': pre_ingestion_result,
        'ingestion_result': ingestion_result,
    }
    return pipeline_result
