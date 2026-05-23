from pathlib import Path
from typing import Any


ML_TRAINING_REPORT_DIR = Path('artifacts/reports/pipeline_3/training')


def format_model_params(
    model_params_json: dict[str, Any] | None,
) -> str:
    """Format model parameters for markdown table.
    Args:
        model_params_json (dict[str, Any] | None): Model parameters.
    """
    if not model_params_json:
        return '| Parameter | Value |\n|---|---:|\n| None | None |'

    rows = [
        '| Parameter | Value |',
        '|---|---:|',
    ]

    for key, value in model_params_json.items():
        rows.append(f'| {key} | {value} |')

    return '\n'.join(rows)


def build_ml_training_report_content(
    training_run_name: str,
    ml_dataset_run_id: int | None,
    client_id: int,
    status: str,
    is_success: bool,
    model_type: str,
    target_name: str,
    model_params_json: dict[str, Any] | None,
    train_row_count: int,
    test_row_count: int,
    metric_mae: float | None,
    metric_rmse: float | None,
    metric_r2: float | None,
    baseline_mae: float | None,
    mean_target: float | None,
    model_path: str | None,
) -> str:
    """Build ML training report content.
    Args:
        training_run_name (str): ML training run name.
        ml_dataset_run_id (int | None): ML dataset run identifier.
        client_id (int): Client identifier.
        status (str): Training status.
        is_success (bool): Whether training run was successful.
        model_type (str): Model type.
        target_name (str): Target name.
        model_params_json (dict[str, Any] | None): Model parameters.
        train_row_count (int): Number of train rows.
        test_row_count (int): Number of test rows.
        metric_mae (float | None): MAE metric.
        metric_rmse (float | None): RMSE metric.
        metric_r2 (float | None): R2 metric.
        baseline_mae (float | None): Baseline MAE metric.
        mean_target (float | None): Mean train target.
        model_path (str | None): Model artifact path.
    """
    formatted_model_params = format_model_params(
        model_params_json=model_params_json,
    )

    return f"""# Pipeline 3 - ML Training Report

## Run Metadata

| Field | Value |
|---|---:|
| Training Run Name | {training_run_name} |
| ML Dataset Run ID | {ml_dataset_run_id} |
| Client ID | {client_id} |
| Status | {status} |
| Success | {is_success} |

## Model

| Field | Value |
|---|---:|
| Model Type | {model_type} |
| Target | {target_name} |
| Model Path | {model_path} |

## Model Parameters

{formatted_model_params}

## Dataset Split

| Field | Value |
|---|---:|
| Train Rows | {train_row_count} |
| Test Rows | {test_row_count} |
| Mean Train Target | {mean_target} |

## Metrics

| Metric | Value |
|---|---:|
| MAE | {metric_mae} |
| RMSE | {metric_rmse} |
| R2 | {metric_r2} |
| Baseline MAE | {baseline_mae} |

## Notes

This report documents one Pipeline 3 ML training run.

Pipeline 3 uses the materialized ML dataset produced by Pipeline 2
from ml_feature_rows.
It does not recalculate feature engineering layers during model training.

The current model is a baseline CatBoostRegressor
for regression on the target callbacks.
"""


def save_ml_training_report(
    report_name: str,
    report_content: str,
) -> str:
    """Save ML training report.
    Args:
        report_name (str): Report file name.
        report_content (str): Report markdown content.
    """
    ML_TRAINING_REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path = ML_TRAINING_REPORT_DIR / report_name
    report_path.write_text(
        report_content,
        encoding='utf-8',
    )

    return str(report_path)
