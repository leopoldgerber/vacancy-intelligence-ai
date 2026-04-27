from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.validation import ValidationUploadResponse
from app.core.exceptions import FileReadError
from app.core.exceptions import InvalidFileExtensionError
from app.core.exceptions import MissingFileNameError
from app.core.exceptions import ValidationExecutionError
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
        raise MissingFileNameError()

    check_xlsx_file(file_name=file.filename)

    file_bytes = await file.read()
    data = read_xlsx_to_dataframe(file_bytes=file_bytes)

    validation_name = file.filename.replace(
        '.xlsx',
        '_validation',
    )
    report_name = file.filename.replace(
        '.xlsx',
        '_validation.md',
    )

    try:
        validation_result = await validate_data(
            session=session,
            data=data,
            validation_name=validation_name,
            source_name=file.filename,
            report_name=report_name,
            required_columns=REQUIRED_COLUMNS,
        )
    except IntegrityError as exc:
        await session.rollback()
        raise ValidationExecutionError(
            detail='Validation failed due to database integrity error.',
        ) from exc
    except SQLAlchemyError as exc:
        await session.rollback()
        raise ValidationExecutionError(
            detail='Validation failed due to database error.',
        ) from exc
    except Exception as exc:
        await session.rollback()
        raise ValidationExecutionError() from exc

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
