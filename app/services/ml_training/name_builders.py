from datetime import datetime


def build_ml_training_run_name() -> str:
    """Build ML training run name.
    Args:
        """
    current_datetime = datetime.now()

    return current_datetime.strftime('ml_training_%Y-%m-%d_%H-%M-%S')


def build_ml_training_report_name(training_run_name: str) -> str:
    """Build ML training report name.
    Args:
        training_run_name (str): ML training run name.
    """
    return f'{training_run_name}.md'
