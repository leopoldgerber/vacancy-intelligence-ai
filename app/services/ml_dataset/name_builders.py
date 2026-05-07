from datetime import datetime


def build_ml_dataset_run_name() -> str:
    """Build ML dataset run name.
    Args:
        """
    current_datetime = datetime.now()

    return current_datetime.strftime('ml_dataset_%Y-%m-%d_%H-%M-%S')


def build_ml_dataset_report_name(dataset_run_name: str) -> str:
    """Build ML dataset report name.
    Args:
        dataset_run_name (str): ML dataset run name.
    """
    return f'{dataset_run_name}.md'
