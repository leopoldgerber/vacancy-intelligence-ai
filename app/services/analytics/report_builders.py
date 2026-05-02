from app.db.models.analytics_run import AnalyticsRun


def build_analytics_report(analytics_run: AnalyticsRun) -> str:
    """Build analytics report content.
    Args:
        analytics_run (AnalyticsRun): Analytics run model.
    """
    report_lines = [
        '# Pipeline 2 Analytics Report',
        '',
        '## Run information',
        '',
        f'- Analytics run ID: {analytics_run.id}',
        f'- Analytics name: {analytics_run.analytics_name}',
        f'- Client ID: {analytics_run.client_id}',
        f'- Date from: {analytics_run.date_from}',
        f'- Date to: {analytics_run.date_to}',
        f'- Status: {analytics_run.status}',
        f'- Is success: {analytics_run.is_success}',
        f'- Snapshot count: {analytics_run.snapshot_count}',
        f'- Report name: {analytics_run.report_name}',
        f'- Created at: {analytics_run.created_at}',
        '',
    ]

    return '\n'.join(report_lines)
