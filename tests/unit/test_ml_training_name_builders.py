from app.services.ml_training.name_builders import (
    build_ml_training_report_name,
)
from app.services.ml_training.name_builders import build_ml_training_run_name


def test_build_ml_training_run_name() -> None:
    """Test ML training run name builder.
    Args:
        """
    result = build_ml_training_run_name()

    assert result.startswith('ml_training_')
    assert len(result) == len('ml_training_2026-05-16_12-00-00')


def test_build_ml_training_report_name() -> None:
    """Test ML training report name builder.
    Args:
        """
    result = build_ml_training_report_name(
        training_run_name='ml_training_test',
    )

    assert result == 'ml_training_test.md'
