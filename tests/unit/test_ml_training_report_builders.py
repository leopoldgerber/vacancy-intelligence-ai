from pathlib import Path

from app.services.ml_training.report_builders import (
    build_ml_training_report_content,
)
from app.services.ml_training.report_builders import format_model_params
from app.services.ml_training.report_builders import save_ml_training_report


CATBOOST_BASELINE_PARAMS = {
    'iterations': 100,
    'learning_rate': 0.05,
    'depth': 6,
    'loss_function': 'RMSE',
    'random_seed': 42,
    'verbose': False,
    'allow_writing_files': False,
}


def test_format_model_params() -> None:
    """Test model params formatter.
    Args:
        """
    result = format_model_params(
        model_params_json=CATBOOST_BASELINE_PARAMS,
    )

    assert '| Parameter | Value |' in result
    assert '| iterations | 100 |' in result
    assert '| learning_rate | 0.05 |' in result
    assert '| depth | 6 |' in result
    assert '| loss_function | RMSE |' in result
    assert '| random_seed | 42 |' in result
    assert '| verbose | False |' in result
    assert '| allow_writing_files | False |' in result


def test_format_model_params_empty() -> None:
    """Test empty model params formatter.
    Args:
        """
    result = format_model_params(model_params_json=None)

    assert '| Parameter | Value |' in result
    assert '| None | None |' in result


def test_build_ml_training_report_content() -> None:
    """Test ML training report content builder.
    Args:
        """
    result = build_ml_training_report_content(
        training_run_name='ml_training_test',
        ml_dataset_run_id=1,
        client_id=1,
        status='success',
        is_success=True,
        model_type='catboost_regressor',
        target_name='callbacks',
        model_params_json=CATBOOST_BASELINE_PARAMS,
        train_row_count=80,
        test_row_count=20,
        metric_mae=0.3,
        metric_rmse=0.6,
        metric_r2=0.1,
        baseline_mae=0.4,
        mean_target=10.0,
        model_path='artifacts/models/pipeline_3/ml_training_test.cbm',
    )

    assert '# Pipeline 3 - ML Training Report' in result
    assert 'ml_training_test' in result
    assert 'catboost_regressor' in result
    assert 'callbacks' in result
    assert '| iterations | 100 |' in result
    assert '| learning_rate | 0.05 |' in result
    assert '80' in result
    assert '20' in result
    assert '10.0' in result
    assert '0.3' in result
    assert '0.6' in result
    assert '0.1' in result
    assert '0.4' in result
    assert '```' not in result


def test_save_ml_training_report() -> None:
    """Test ML training report saving.
    Args:
        """
    report_name = 'ml_training_test_report.md'
    report_content = '# Test Report'

    report_path = save_ml_training_report(
        report_name=report_name,
        report_content=report_content,
    )

    path = Path(report_path)

    assert path.exists()
    assert path.is_file()
    assert path.name == report_name
    assert path.read_text(encoding='utf-8') == report_content

    path.unlink()
