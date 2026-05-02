from datetime import datetime


def build_analytics_name() -> str:
    """Build analytics run name.
    Args:
        """
    current_datetime = datetime.now()

    return current_datetime.strftime('analytics_%Y-%m-%d_%H-%M-%S')


def build_analytics_report_name(analytics_name: str) -> str:
    """Build analytics report name.
    Args:
        analytics_name (str): Analytics run name.
    """
    return f'{analytics_name}.md'
