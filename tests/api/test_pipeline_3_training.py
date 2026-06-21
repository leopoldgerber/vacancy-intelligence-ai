from typing import Any
from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def build_prediction_diagnostics_json() -> dict[str, Any]:
    """Build prediction diagnostics json for API tests.
    Args:
        """
    return {
        'prediction_row_count': 20,
        'mean_prediction_error': 0.0,
        'mean_absolute_error': 0.31,
        'max_absolute_error': 2.0,
        'mean_squared_error': 0.75,
        'root_mean_squared_error': 0.8660254037844386,
        'over_prediction_count': 9,
        'under_prediction_count': 11,
        'mean_absolute_error_by_profile': {
            'Verkäufer': 0.28,
            'Filialleiter': 0.42,
        },
        'mean_absolute_error_by_city': {
            'Berlin': 0.3,
            'Hamburg': 0.35,
        },
        'mean_absolute_error_by_company_id': {
            '57': 0.28,
            '58': 0.42,
        },
        'top_worst_predictions': [
            {
                'source_row_index': 10,
                'client_id': 1,
                'company_id': 57,
                'vacancy_id': 17,
                'date_day': '2025-08-20T00:00:00',
                'profile': 'Verkäufer',
                'city': 'Berlin',
                'actual_value': 3.0,
                'predicted_value': 1.0,
                'prediction_error': -2.0,
                'absolute_error': 2.0,
                'squared_error': 4.0,
            },
        ],
    }


def test_pipeline_3_training_run_success(monkeypatch) -> None:
    """Test successful Pipeline 3 training endpoint.
    Args:
        monkeypatch: Pytest monkeypatch fixture.
    """
    prediction_diagnostics_json = build_prediction_diagnostics_json()

    mock_result = {
        'ml_training_run_id': 1,
        'training_run_name': 'ml_training_2026-06-19_21-23-09',
        'status': 'success',
        'is_success': True,
        'model_type': 'catboost_regressor',
        'target_name': 'callbacks',
        'model_params_json': {
            'iterations': 100,
            'learning_rate': 0.05,
            'depth': 6,
        },
        'feature_importance_json': {
            'salary_mid': 18.7,
            'description_length': 11.1,
        },
        'prediction_diagnostics_json': prediction_diagnostics_json,
        'train_row_count': 80,
        'test_row_count': 20,
        'prediction_row_count': 20,
        'metric_mae': 0.31,
        'metric_rmse': 0.86,
        'metric_r2': 0.09,
        'baseline_mae': 0.33,
        'mean_target': 0.21,
        'model_path': 'artifacts/models/pipeline_3/model.cbm',
        'report_name': 'ml_training_2026-06-19_21-23-09.md',
    }

    mock_run_ml_training = AsyncMock(return_value=mock_result)

    monkeypatch.setattr(
        'app.api.routes.ml_training.run_ml_training',
        mock_run_ml_training,
    )

    response = client.post(
        '/pipeline-3/training/run',
        data={
            'client_id': '1',
            'ml_dataset_run_id': '',
        },
    )

    assert response.status_code == 200
    assert response.json() == mock_result

    mock_run_ml_training.assert_awaited_once()


def test_pipeline_3_training_run_with_ml_dataset_run_id(
    monkeypatch,
) -> None:
    """Test Pipeline 3 training endpoint with explicit ML dataset run id.
    Args:
        monkeypatch: Pytest monkeypatch fixture.
    """
    prediction_diagnostics_json = build_prediction_diagnostics_json()
    prediction_diagnostics_json['prediction_row_count'] = 998

    mock_result = {
        'ml_training_run_id': 2,
        'training_run_name': 'ml_training_2026-06-21_18-56-23',
        'status': 'success',
        'is_success': True,
        'model_type': 'catboost_regressor',
        'target_name': 'callbacks',
        'model_params_json': {
            'iterations': 100,
            'learning_rate': 0.05,
            'depth': 6,
        },
        'feature_importance_json': {
            'salary_mid': 18.70667672292487,
            'description_length': 11.110646939920215,
        },
        'prediction_diagnostics_json': prediction_diagnostics_json,
        'train_row_count': 3349,
        'test_row_count': 998,
        'prediction_row_count': 998,
        'metric_mae': 0.3191556270424175,
        'metric_rmse': 0.8702502638996834,
        'metric_r2': 0.09774647610811327,
        'baseline_mae': 0.33083126539732194,
        'mean_target': 0.21021200358315914,
        'model_path': (
            'artifacts/models/pipeline_3/'
            'ml_training_2026-06-21_18-56-23.cbm'
        ),
        'report_name': 'ml_training_2026-06-21_18-56-23.md',
    }

    mock_run_ml_training = AsyncMock(return_value=mock_result)

    monkeypatch.setattr(
        'app.api.routes.ml_training.run_ml_training',
        mock_run_ml_training,
    )

    response = client.post(
        '/pipeline-3/training/run',
        data={
            'client_id': '1',
            'ml_dataset_run_id': '26',
        },
    )

    assert response.status_code == 200
    assert response.json() == mock_result

    mock_run_ml_training.assert_awaited_once()


def test_pipeline_3_training_run_no_data(monkeypatch) -> None:
    """Test Pipeline 3 training endpoint with no data.
    Args:
        monkeypatch: Pytest monkeypatch fixture.
    """
    mock_result = {
        'ml_training_run_id': 3,
        'training_run_name': 'ml_training_2026-06-21_19-00-00',
        'status': 'no_data',
        'is_success': False,
        'model_type': 'catboost_regressor',
        'target_name': 'callbacks',
        'model_params_json': {
            'iterations': 100,
            'learning_rate': 0.05,
            'depth': 6,
        },
        'feature_importance_json': None,
        'prediction_diagnostics_json': None,
        'train_row_count': 0,
        'test_row_count': 0,
        'prediction_row_count': 0,
        'metric_mae': None,
        'metric_rmse': None,
        'metric_r2': None,
        'baseline_mae': None,
        'mean_target': None,
        'model_path': None,
        'report_name': 'ml_training_2026-06-21_19-00-00.md',
    }

    mock_run_ml_training = AsyncMock(return_value=mock_result)

    monkeypatch.setattr(
        'app.api.routes.ml_training.run_ml_training',
        mock_run_ml_training,
    )

    response = client.post(
        '/pipeline-3/training/run',
        data={
            'client_id': '1',
            'ml_dataset_run_id': '',
        },
    )

    assert response.status_code == 200
    assert response.json() == mock_result

    mock_run_ml_training.assert_awaited_once()
