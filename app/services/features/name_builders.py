from datetime import datetime


def build_feature_run_name() -> str:
    """Build feature engineering run name.
    Args:
        """
    current_datetime = datetime.now()

    return current_datetime.strftime('features_%Y-%m-%d_%H-%M-%S')


def build_feature_report_name(feature_run_name: str) -> str:
    """Build feature engineering report name.
    Args:
        feature_run_name (str): Feature engineering run name.
    """
    return f'{feature_run_name}.md'
