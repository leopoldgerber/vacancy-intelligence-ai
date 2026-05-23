import pytest
from httpx import ASGITransport
from httpx import AsyncClient

from app.api.main import app


@pytest.mark.asyncio
async def test_pipeline_3_training_success(
    monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test Pipeline 3 training endpoint success response.
    Args:
        monkeypatch (pytest.MonkeyPatch): Pytest monkeypatch fixture.
    """
    async def mock_run_ml_training(
        client_id: int,
        ml_dataset_run_id: int | None = None,
    ) -> dict[str, int | str | bool | float | None]:
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
            'train_row_count': 80,
            'test_row_count': 20,
            'metric_mae': 0.3,
            'metric_rmse': 0.6,
            'metric_r2': 0.1,
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
        'train_row_count': 80,
        'test_row_count': 20,
        'metric_mae': 0.3,
        'metric_rmse': 0.6,
        'metric_r2': 0.1,
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
    ) -> dict[str, int | str | bool | float | None]:
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
            'train_row_count': 3349,
            'test_row_count': 998,
            'metric_mae': 0.3208829917467808,
            'metric_rmse': 0.6562405923499849,
            'metric_r2': 0.0023936394210444245,
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

    assert response_data['ml_training_run_id'] == 2
    assert response_data['training_run_name'] == (
        'ml_training_test_with_dataset'
    )
    assert response_data['status'] == 'success'
    assert response_data['is_success'] is True
    assert response_data['model_type'] == 'catboost_regressor'
    assert response_data['target_name'] == 'callbacks'
    assert response_data['train_row_count'] == 3349
    assert response_data['test_row_count'] == 998
    assert response_data['metric_mae'] == 0.3208829917467808
    assert response_data['metric_rmse'] == 0.6562405923499849
    assert response_data['metric_r2'] == 0.0023936394210444245
    assert response_data['model_path'] == (
        'artifacts/models/pipeline_3/ml_training_test_with_dataset.cbm'
    )
    assert response_data['report_name'] == (
        'ml_training_test_with_dataset.md'
    )


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
    ) -> dict[str, int | str | bool | float | None]:
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
            'train_row_count': 0,
            'test_row_count': 0,
            'metric_mae': None,
            'metric_rmse': None,
            'metric_r2': None,
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
        'train_row_count': 0,
        'test_row_count': 0,
        'metric_mae': None,
        'metric_rmse': None,
        'metric_r2': None,
        'model_path': None,
        'report_name': 'ml_training_no_data.md',
    }
