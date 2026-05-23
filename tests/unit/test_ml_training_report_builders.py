from pathlib import Path

from app.services.ml_training.report_builders import (
    build_ml_training_report_content,
)
from app.services.ml_training.report_builders import save_ml_training_report


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
        train_row_count=80,
        test_row_count=20,
        metric_mae=0.3,
        metric_rmse=0.6,
        metric_r2=0.1,
        model_path='artifacts/models/pipeline_3/ml_training_test.cbm',
    )

    assert '# Pipeline 3 - ML Training Report' in result
    assert 'ml_training_test' in result
    assert 'catboost_regressor' in result
    assert 'callbacks' in result
    assert '80' in result
    assert '20' in result
    assert '0.3' in result
    assert '0.6' in result
    assert '0.1' in result


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
