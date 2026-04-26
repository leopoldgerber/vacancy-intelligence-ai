from collections.abc import Sequence

import pandas as pd

from app.services.data_validation.field_checks import (
    run_blocking_field_checks,
    run_warning_field_checks,
)
from app.services.data_validation.result_builders import (
    build_validation_result,
)
from app.services.data_validation.schema_checks import run_schema_checks


def run_validation(
    data: pd.DataFrame,
    validation_name: str,
    source_name: str,
    report_name: str,
    required_columns: list[str],
    client_ids: Sequence[int],
    datetime_format: str = '%Y-%m-%d %H:%M:%S',
) -> dict[str, dict[str, str | int | bool] | dict[str, int]]:
    """Run full data validation process.
    Args:
        data (pd.DataFrame): Input dataset.
        validation_name (str): Validation run name.
        source_name (str): Source dataset name.
        report_name (str): Markdown report name.
        required_columns (list[str]): Required dataset columns.
        client_ids (Sequence[int]): Valid client identifiers.
        datetime_format (str): Datetime format for validation."""
    schema_results = run_schema_checks(
        data=data,
        required_columns=required_columns,
    )

    blocking_results = run_blocking_field_checks(
        data=data,
        client_ids=client_ids,
        datetime_format=datetime_format,
    )

    warning_results = run_warning_field_checks(data=data)

    validation_result = build_validation_result(
        data=data,
        validation_name=validation_name,
        source_name=source_name,
        report_name=report_name,
        schema_results=schema_results,
        blocking_results=blocking_results,
        warning_results=warning_results,
    )
    return validation_result
