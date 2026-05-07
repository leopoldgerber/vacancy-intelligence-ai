from datetime import datetime


def build_feature_run_name(feature_group: str) -> str:
    """Build feature engineering run name.
    Args:
        feature_group (str): Feature group name.
    """
    current_datetime = datetime.now()

    return current_datetime.strftime(
        f'{feature_group}_%Y-%m-%d_%H-%M-%S',
    )


def build_feature_report_name(feature_run_name: str) -> str:
    """Build feature engineering report name.
    Args:
        feature_run_name (str): Feature engineering run name.
    """
    return f'{feature_run_name}.md'
