from datetime import datetime
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.validation import ValidationUploadResponse
from app.db.session import get_session
from app.services.data_validation.constants import REQUIRED_COLUMNS
from app.services.data_validation.service import validate_data


router = APIRouter(prefix='/validation', tags=['validation'])


def check_xlsx_file(file_name: str) -> None:
    """Check that uploaded file has xlsx extension.
    Args:
        file_name (str): Uploaded file name."""
    is_xlsx = file_name.lower().endswith('.xlsx')

    if not is_xlsx:
        raise HTTPException(
            status_code=400,
            detail='Only .xlsx files are allowed.',
        )


def read_xlsx_to_dataframe(file_bytes: bytes) -> pd.DataFrame:
    """Read xlsx bytes into DataFrame.
    Args:
        file_bytes (bytes): Uploaded file content."""
    data = pd.read_excel(BytesIO(file_bytes))
    return data


def build_operation_name(operation_name: str) -> str:
    """Build operation name with current timestamp.
    Args:
        operation_name (str): Operation name prefix."""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    operation_value = f'{operation_name}_{timestamp}'
    return operation_value


@router.post('/upload', response_model=ValidationUploadResponse)
async def validate_uploaded_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
) -> ValidationUploadResponse:
    """Validate uploaded xlsx file.
    Args:
        file (UploadFile): Uploaded xlsx file.
        session (AsyncSession): Async database session."""
    if file.filename is None:
        raise HTTPException(
            status_code=400,
            detail='Uploaded file name is missing.',
        )

    check_xlsx_file(file_name=file.filename)

    file_bytes = await file.read()
    data = read_xlsx_to_dataframe(file_bytes=file_bytes)

    validation_name = build_operation_name(operation_name='validation')
    report_name = f'{validation_name}.md'

    validation_result = await validate_data(
        session=session,
        data=data,
        validation_name=validation_name,
        source_name=file.filename,
        report_name=report_name,
        required_columns=REQUIRED_COLUMNS,
    )

    if not validation_result['is_valid']:
        return ValidationUploadResponse(
            status='failed',
            message='Validation failed.',
            validation_run_id=validation_result['validation_run'].id,
            report_path=validation_result['report_path'],
        )

    return ValidationUploadResponse(
        status='ok',
        message='Validation completed successfully.',
        validation_run_id=validation_result['validation_run'].id,
        report_path=validation_result['report_path'],
    )
