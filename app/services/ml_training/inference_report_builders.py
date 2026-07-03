from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any


if TYPE_CHECKING:
    from app.services.ml_training.run_ml_inference_pipeline import (
        MlInferencePipelineResult,
    )


@dataclass
class InferencePredictionSummary:
    """Inference prediction summary."""

    prediction_count: int
    mean_prediction: float | None
    min_prediction: float | None
    max_prediction: float | None


def format_value(value: Any) -> str:
    """Format report value.
    Args:
        value (Any): Source value."""
    if value is None:
        return ''

    if isinstance(value, float):
        return f'{value:.6f}'

    if hasattr(value, 'isoformat'):
        return value.isoformat()

    return str(value)


def summarize_predictions(
    predictions: list[float],
) -> InferencePredictionSummary:
    """Summarize inference predictions.
    Args:
        predictions (list[float]): Inference prediction values."""
    if not predictions:
        return InferencePredictionSummary(
            prediction_count=0,
            mean_prediction=None,
            min_prediction=None,
            max_prediction=None,
        )

    prediction_count = len(predictions)
    mean_prediction = sum(predictions) / prediction_count

    return InferencePredictionSummary(
        prediction_count=prediction_count,
        mean_prediction=mean_prediction,
        min_prediction=min(predictions),
        max_prediction=max(predictions),
    )


def build_metadata_table(
    result: 'MlInferencePipelineResult',
) -> str:
    """Build inference metadata table.
    Args:
        result (MlInferencePipelineResult): ML inference pipeline result."""
    rows = [
        ('ML Training Run ID', result.ml_training_run_id),
        ('Training Run Name', result.training_run_name),
        ('ML Dataset Run ID', result.ml_dataset_run_id),
        ('Client ID', result.client_id),
        ('Model Path', result.model_path),
        ('Source Rows', result.row_count),
        ('Prediction Rows', result.prediction_row_count),
        ('Report Name', result.report_name),
        ('Report Path', result.report_path),
    ]

    table_rows = [
        '| Metric | Value |',
        '|---|---|',
    ]

    for metric_name, metric_value in rows:
        table_rows.append(
            f'| {metric_name} | {format_value(metric_value)} |',
        )

    return '\n'.join(table_rows)


def build_summary_table(
    summary: InferencePredictionSummary,
) -> str:
    """Build prediction summary table.
    Args:
        summary (InferencePredictionSummary): Prediction summary."""
    rows = [
        ('Prediction Count', summary.prediction_count),
        ('Mean Prediction', summary.mean_prediction),
        ('Min Prediction', summary.min_prediction),
        ('Max Prediction', summary.max_prediction),
    ]

    table_rows = [
        '| Metric | Value |',
        '|---|---|',
    ]

    for metric_name, metric_value in rows:
        table_rows.append(
            f'| {metric_name} | {format_value(metric_value)} |',
        )

    return '\n'.join(table_rows)


def build_prediction_table(
    prediction_rows: list[dict[str, Any]],
    limit: int = 10,
) -> str:
    """Build sample prediction rows table.
    Args:
        prediction_rows (list[dict[str, Any]]): Inference prediction rows.
        limit (int): Maximum number of rows to render."""
    if not prediction_rows:
        return 'No prediction rows.'

    columns = [
        'source_row_index',
        'client_id',
        'company_id',
        'vacancy_id',
        'date_day',
        'predicted_value',
    ]
    table_rows = [
        (
            '| Source Row | Client ID | Company ID | '
            'Vacancy ID | Date | Prediction |'
        ),
        '|---|---|---|---|---|---|',
    ]

    for prediction_row in prediction_rows[:limit]:
        values = [
            format_value(prediction_row.get(column))
            for column in columns
        ]
        table_rows.append(
            '| '
            + ' | '.join(values)
            + ' |',
        )

    return '\n'.join(table_rows)


def build_inference_report(
    result: 'MlInferencePipelineResult',
) -> str:
    """Build ML inference markdown report.
    Args:
        result (MlInferencePipelineResult): ML inference pipeline result."""
    summary = summarize_predictions(predictions=result.predictions)
    metadata_table = build_metadata_table(result=result)
    summary_table = build_summary_table(summary=summary)
    prediction_table = build_prediction_table(
        prediction_rows=result.prediction_rows,
    )

    report_parts = [
        '# ML Inference Report',
        '',
        '## Run Metadata',
        '',
        metadata_table,
        '',
        '## Prediction Summary',
        '',
        summary_table,
        '',
        '## Sample Predictions',
        '',
        prediction_table,
        '',
    ]

    return '\n'.join(report_parts)
