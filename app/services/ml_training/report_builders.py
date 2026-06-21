from pathlib import Path
from typing import Any


ML_TRAINING_REPORT_DIR = Path('artifacts/reports/pipeline_3/training')
MAX_GROUP_ERROR_ROW_COUNT = 10


def format_model_params(
    model_params_json: dict[str, Any] | None,
) -> str:
    """Format model parameters for markdown table.
    Args:
        model_params_json (dict[str, Any] | None):
            Model parameters.
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


def format_feature_importance(
    feature_importance_json: dict[str, Any] | None,
) -> str:
    """Format feature importance for markdown table.
    Args:
        feature_importance_json (dict[str, Any] | None):
            Feature importance.
    """
    if not feature_importance_json:
        return '| Feature | Importance |\n|---|---:|\n| None | None |'

    rows = [
        '| Feature | Importance |',
        '|---|---:|',
    ]

    for feature_name, importance_value in feature_importance_json.items():
        rows.append(f'| {feature_name} | {importance_value} |')

    return '\n'.join(rows)


def format_prediction_diagnostics(
    prediction_diagnostics_json: dict[str, Any] | None,
) -> str:
    """Format prediction diagnostics for markdown table.
    Args:
        prediction_diagnostics_json (dict[str, Any] | None):
            Prediction diagnostics.
    """
    if not prediction_diagnostics_json:
        return '| Metric | Value |\n|---|---:|\n| None | None |'

    rows = [
        '| Metric | Value |',
        '|---|---:|',
        (
            '| Prediction Rows | '
            f'{prediction_diagnostics_json.get("prediction_row_count")} |'
        ),
        (
            '| Mean Prediction Error | '
            f'{prediction_diagnostics_json.get("mean_prediction_error")} |'
        ),
        (
            '| Mean Absolute Error | '
            f'{prediction_diagnostics_json.get("mean_absolute_error")} |'
        ),
        (
            '| Max Absolute Error | '
            f'{prediction_diagnostics_json.get("max_absolute_error")} |'
        ),
        (
            '| Mean Squared Error | '
            f'{prediction_diagnostics_json.get("mean_squared_error")} |'
        ),
        (
            '| Root Mean Squared Error | '
            f'{prediction_diagnostics_json.get("root_mean_squared_error")} |'
        ),
        (
            '| Over Prediction Count | '
            f'{prediction_diagnostics_json.get("over_prediction_count")} |'
        ),
        (
            '| Under Prediction Count | '
            f'{prediction_diagnostics_json.get("under_prediction_count")} |'
        ),
    ]

    return '\n'.join(rows)


def format_group_errors(
    group_errors_json: dict[str, Any] | None,
    group_label: str,
) -> str:
    """Format grouped prediction errors for markdown table.
    Args:
        group_errors_json (dict[str, Any] | None):
            Grouped prediction errors.
        group_label (str):
            Group label.
    """
    if not group_errors_json:
        return f'| {group_label} | Mean Absolute Error |\n|---|---:|\n| None | None |'

    rows = [
        f'| {group_label} | Mean Absolute Error |',
        '|---|---:|',
    ]

    group_error_items = list(group_errors_json.items())[
        :MAX_GROUP_ERROR_ROW_COUNT
    ]

    for group_name, error_value in group_error_items:
        rows.append(f'| {group_name} | {error_value} |')

    return '\n'.join(rows)


def format_top_worst_predictions(
    prediction_diagnostics_json: dict[str, Any] | None,
) -> str:
    """Format top worst predictions for markdown table.
    Args:
        prediction_diagnostics_json (dict[str, Any] | None):
            Prediction diagnostics.
    """
    if not prediction_diagnostics_json:
        return (
            '| Rank | Vacancy ID | Company ID | Profile | City | Actual | '
            'Predicted | Error | Absolute Error |\n'
            '|---:|---:|---:|---|---|---:|---:|---:|---:|\n'
            '| None | None | None | None | None | None | None | None | None |'
        )

    worst_predictions = prediction_diagnostics_json.get(
        'top_worst_predictions',
    )

    if not worst_predictions:
        return (
            '| Rank | Vacancy ID | Company ID | Profile | City | Actual | '
            'Predicted | Error | Absolute Error |\n'
            '|---:|---:|---:|---|---|---:|---:|---:|---:|\n'
            '| None | None | None | None | None | None | None | None | None |'
        )

    rows = [
        (
            '| Rank | Vacancy ID | Company ID | Profile | City | Actual | '
            'Predicted | Error | Absolute Error |'
        ),
        '|---:|---:|---:|---|---|---:|---:|---:|---:|',
    ]

    for rank, prediction in enumerate(worst_predictions, start=1):
        rows.append(
            (
                f'| {rank} | '
                f'{prediction.get("vacancy_id")} | '
                f'{prediction.get("company_id")} | '
                f'{prediction.get("profile")} | '
                f'{prediction.get("city")} | '
                f'{prediction.get("actual_value")} | '
                f'{prediction.get("predicted_value")} | '
                f'{prediction.get("prediction_error")} | '
                f'{prediction.get("absolute_error")} |'
            ),
        )

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
    feature_importance_json: dict[str, Any] | None,
    train_row_count: int,
    test_row_count: int,
    metric_mae: float | None,
    metric_rmse: float | None,
    metric_r2: float | None,
    baseline_mae: float | None,
    mean_target: float | None,
    model_path: str | None,
    prediction_row_count: int = 0,
    prediction_diagnostics_json: dict[str, Any] | None = None,
) -> str:
    """Build ML training report content.
    Args:
        training_run_name (str):
            ML training run name.
        ml_dataset_run_id (int | None):
            ML dataset run identifier.
        client_id (int):
            Client identifier.
        status (str):
            Training status.
        is_success (bool):
            Whether training run was successful.
        model_type (str):
            Model type.
        target_name (str):
            Target name.
        model_params_json (dict[str, Any] | None):
            Model parameters.
        feature_importance_json (dict[str, Any] | None):
            Feature importance.
        train_row_count (int):
            Number of train rows.
        test_row_count (int):
            Number of test rows.
        metric_mae (float | None):
            MAE metric.
        metric_rmse (float | None):
            RMSE metric.
        metric_r2 (float | None):
            R2 metric.
        baseline_mae (float | None):
            Baseline MAE metric.
        mean_target (float | None):
            Mean train target.
        model_path (str | None):
            Model artifact path.
        prediction_row_count (int):
            Number of saved prediction rows.
        prediction_diagnostics_json (dict[str, Any] | None):
            Prediction diagnostics.
    """
    formatted_model_params = format_model_params(
        model_params_json=model_params_json,
    )
    formatted_feature_importance = format_feature_importance(
        feature_importance_json=feature_importance_json,
    )
    formatted_prediction_diagnostics = format_prediction_diagnostics(
        prediction_diagnostics_json=prediction_diagnostics_json,
    )
    formatted_profile_errors = format_group_errors(
        group_errors_json=(
            prediction_diagnostics_json or {}
        ).get('mean_absolute_error_by_profile'),
        group_label='Profile',
    )
    formatted_city_errors = format_group_errors(
        group_errors_json=(
            prediction_diagnostics_json or {}
        ).get('mean_absolute_error_by_city'),
        group_label='City',
    )
    formatted_company_errors = format_group_errors(
        group_errors_json=(
            prediction_diagnostics_json or {}
        ).get('mean_absolute_error_by_company_id'),
        group_label='Company ID',
    )
    formatted_top_worst_predictions = format_top_worst_predictions(
        prediction_diagnostics_json=prediction_diagnostics_json,
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

## Feature Importance

{formatted_feature_importance}

## Dataset Split

| Field | Value |
|---|---:|
| Train Rows | {train_row_count} |
| Test Rows | {test_row_count} |
| Prediction Rows | {prediction_row_count} |
| Mean Train Target | {mean_target} |

## Prediction Diagnostics

{formatted_prediction_diagnostics}

## Mean Absolute Error by Profile

{formatted_profile_errors}

## Mean Absolute Error by City

{formatted_city_errors}

## Mean Absolute Error by Company

{formatted_company_errors}

## Top Worst Predictions

{formatted_top_worst_predictions}

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
        report_name (str):
            Report file name.
        report_content (str):
            Report markdown content.
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
