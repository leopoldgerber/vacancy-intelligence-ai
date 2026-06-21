import pytest
from httpx import ASGITransport
from httpx import AsyncClient

from app.api.main import app


CATBOOST_BASELINE_PARAMS = {
    'iterations': 100,
    'learning_rate': 0.05,
    'depth': 6,
    'loss_function': 'RMSE',
    'random_seed': 42,
    'verbose': False,
    'allow_writing_files': False,
}

FEATURE_IMPORTANCE_JSON = {
    'salary_mid': 22.5,
    'publication_hour': 14.2,
    'city': 9.8,
}


@pytest.mark.asyncio
async def test_pipeline_3_training_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test Pipeline 3 training endpoint success response.
    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
    """
    async def mock_run_ml_training(
        client_id: int,
        ml_dataset_run_id: int | None = None,
    ) -> dict[str, int | str | bool | float | dict[str, object] | None]:
        """Mock ML training service.
        Args:
            client_id (int): Client identifier.
            ml_dataset_run_id (int | None): Optional ML dataset run identifier.
        """
        assert client_id == 1
        assert ml_dataset_run_id is None

        return {
            'ml_training_run_id': 1,
            'training_run_name': 'ml_training_test',
            'status': 'success',
            'is_success': True,
            'model_type': 'catboost_regressor',
            'target_name': 'callbacks',
            'model_params_json': CATBOOST_BASELINE_PARAMS,
            'feature_importance_json': FEATURE_IMPORTANCE_JSON,
            'train_row_count': 80,
            'test_row_count': 20,
            'prediction_row_count': 20,
            'metric_mae': 0.3,
            'metric_rmse': 0.6,
            'metric_r2': 0.1,
            'baseline_mae': 0.4,
            'mean_target': 10.0,
            'model_path': (
                'artifacts/models/pipeline_3/ml_training_test.cbm'
            ),
            'report_name': 'ml_training_test.md',
        }

    monkeypatch.setattr(
        'app.api.routes.ml_training.run_ml_training',
        mock_run_ml_training,
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as client:
        response = await client.post(
            '/pipeline-3/training/run',
            data={
                'client_id': '1',
                'ml_dataset_run_id': '',
            },
        )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data == {
        'ml_training_run_id': 1,
        'training_run_name': 'ml_training_test',
        'status': 'success',
        'is_success': True,
        'model_type': 'catboost_regressor',
        'target_name': 'callbacks',
        'model_params_json': CATBOOST_BASELINE_PARAMS,
        'feature_importance_json': FEATURE_IMPORTANCE_JSON,
        'train_row_count': 80,
        'test_row_count': 20,
        'prediction_row_count': 20,
        'metric_mae': 0.3,
        'metric_rmse': 0.6,
        'metric_r2': 0.1,
        'baseline_mae': 0.4,
        'mean_target': 10.0,
        'model_path': 'artifacts/models/pipeline_3/ml_training_test.cbm',
        'report_name': 'ml_training_test.md',
    }


@pytest.mark.asyncio
async def test_pipeline_3_training_with_dataset_run_id(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test Pipeline 3 training endpoint with ML dataset run id.
    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
    """
    async def mock_run_ml_training(
        client_id: int,
        ml_dataset_run_id: int | None = None,
    ) -> dict[str, int | str | bool | float | dict[str, object] | None]:
        """Mock ML training service.
        Args:
            client_id (int): Client identifier.
            ml_dataset_run_id (int | None): Optional ML dataset run identifier.
        """
        assert client_id == 1
        assert ml_dataset_run_id == 15

        return {
            'ml_training_run_id': 2,
            'training_run_name': 'ml_training_test_with_dataset',
            'status': 'success',
            'is_success': True,
            'model_type': 'catboost_regressor',
            'target_name': 'callbacks',
            'model_params_json': CATBOOST_BASELINE_PARAMS,
            'feature_importance_json': FEATURE_IMPORTANCE_JSON,
            'train_row_count': 3349,
            'test_row_count': 998,
            'prediction_row_count': 998,
            'metric_mae': 0.3208829917467808,
            'metric_rmse': 0.6562405923499849,
            'metric_r2': 0.0023936394210444245,
            'baseline_mae': 0.321,
            'mean_target': 0.42,
            'model_path': (
                'artifacts/models/pipeline_3/'
                'ml_training_test_with_dataset.cbm'
            ),
            'report_name': 'ml_training_test_with_dataset.md',
        }

    monkeypatch.setattr(
        'app.api.routes.ml_training.run_ml_training',
        mock_run_ml_training,
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as client:
        response = await client.post(
            '/pipeline-3/training/run',
            data={
                'client_id': '1',
                'ml_dataset_run_id': '15',
            },
        )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data == {
        'ml_training_run_id': 2,
        'training_run_name': 'ml_training_test_with_dataset',
        'status': 'success',
        'is_success': True,
        'model_type': 'catboost_regressor',
        'target_name': 'callbacks',
        'model_params_json': CATBOOST_BASELINE_PARAMS,
        'feature_importance_json': FEATURE_IMPORTANCE_JSON,
        'train_row_count': 3349,
        'test_row_count': 998,
        'prediction_row_count': 998,
        'metric_mae': 0.3208829917467808,
        'metric_rmse': 0.6562405923499849,
        'metric_r2': 0.0023936394210444245,
        'baseline_mae': 0.321,
        'mean_target': 0.42,
        'model_path': (
            'artifacts/models/pipeline_3/ml_training_test_with_dataset.cbm'
        ),
        'report_name': 'ml_training_test_with_dataset.md',
    }


@pytest.mark.asyncio
async def test_pipeline_3_training_no_data(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test Pipeline 3 training endpoint no-data response.
    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
    """
    async def mock_run_ml_training(
        client_id: int,
        ml_dataset_run_id: int | None = None,
    ) -> dict[str, int | str | bool | float | dict[str, object] | None]:
        """Mock ML training service.
        Args:
            client_id (int): Client identifier.
            ml_dataset_run_id (int | None): Optional ML dataset run identifier.
        """
        assert client_id == 1
        assert ml_dataset_run_id is None

        return {
            'ml_training_run_id': 3,
            'training_run_name': 'ml_training_no_data',
            'status': 'no_data',
            'is_success': False,
            'model_type': 'catboost_regressor',
            'target_name': 'callbacks',
            'model_params_json': CATBOOST_BASELINE_PARAMS,
            'feature_importance_json': None,
            'train_row_count': 0,
            'test_row_count': 0,
            'prediction_row_count': 0,
            'metric_mae': None,
            'metric_rmse': None,
            'metric_r2': None,
            'baseline_mae': None,
            'mean_target': None,
            'model_path': None,
            'report_name': 'ml_training_no_data.md',
        }

    monkeypatch.setattr(
        'app.api.routes.ml_training.run_ml_training',
        mock_run_ml_training,
    )

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url='http://test',
    ) as client:
        response = await client.post(
            '/pipeline-3/training/run',
            data={
                'client_id': '1',
                'ml_dataset_run_id': '',
            },
        )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data == {
        'ml_training_run_id': 3,
        'training_run_name': 'ml_training_no_data',
        'status': 'no_data',
        'is_success': False,
        'model_type': 'catboost_regressor',
        'target_name': 'callbacks',
        'model_params_json': CATBOOST_BASELINE_PARAMS,
        'feature_importance_json': None,
        'train_row_count': 0,
        'test_row_count': 0,
        'prediction_row_count': 0,
        'metric_mae': None,
        'metric_rmse': None,
        'metric_r2': None,
        'baseline_mae': None,
        'mean_target': None,
        'model_path': None,
        'report_name': 'ml_training_no_data.md',
    }
