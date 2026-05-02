from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.pipeline import PipelineUploadResponse
from app.core.exceptions import AppError
from app.core.exceptions import FileReadError
from app.core.exceptions import InvalidFileExtensionError
from app.core.exceptions import MissingFileNameError
from app.core.exceptions import PipelineExecutionError
from app.db.session import get_session
from app.services.pipeline.service import execute_pipeline_1


router = APIRouter(prefix='/pipeline-1', tags=['pipeline'])


def check_xlsx_file(file_name: str) -> None:
    """Check that uploaded file has xlsx extension.
    Args:
        file_name (str): Uploaded file name."""
    is_xlsx = file_name.lower().endswith('.xlsx')

    if not is_xlsx:
        raise InvalidFileExtensionError()


def read_xlsx_to_dataframe(file_bytes: bytes) -> pd.DataFrame:
    """Read xlsx bytes into DataFrame.
    Args:
        file_bytes (bytes): Uploaded file content."""
    try:
        data = pd.read_excel(BytesIO(file_bytes))
    except Exception as exc:
        raise FileReadError() from exc

    return data


@router.post('/run', response_model=PipelineUploadResponse)
async def run_pipeline(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
) -> PipelineUploadResponse:
    """Run pipeline 1 for uploaded xlsx file.
    Args:
        file (UploadFile): Uploaded xlsx file.
        session (AsyncSession): Async database session."""
    if file.filename is None:
        raise MissingFileNameError()

    check_xlsx_file(file_name=file.filename)

    file_bytes = await file.read()
    data = read_xlsx_to_dataframe(file_bytes=file_bytes)

    try:
        pipeline_result = await execute_pipeline_1(
            session=session,
            data=data,
            source_name=file.filename,
        )
    except AppError:
        await session.rollback()
        raise
    except IntegrityError as exc:
        await session.rollback()
        raise PipelineExecutionError(
            detail='Pipeline failed due to database integrity error.',
        ) from exc
    except SQLAlchemyError as exc:
        await session.rollback()
        raise PipelineExecutionError(
            detail='Pipeline failed due to database error.',
        ) from exc
    except Exception as exc:
        await session.rollback()
        raise PipelineExecutionError() from exc

    if pipeline_result['ingestion_result'] is None:
        return PipelineUploadResponse(
            status='failed',
            message='Pipeline 1 failed on pre-ingestion checks.',
            should_ingest=False,
            company_count=None,
            vacancy_count=None,
            snapshot_count=None,
        )

    ingestion_result = pipeline_result['ingestion_result']

    return PipelineUploadResponse(
        status='ok',
        message='Pipeline 1 completed successfully.',
        should_ingest=True,
        company_count=ingestion_result['company_count'],
        vacancy_count=ingestion_result['vacancy_count'],
        snapshot_count=ingestion_result['snapshot_count'],
    )
