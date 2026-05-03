from app.db.models.analytics_run import AnalyticsRun
from app.db.models.market_summary import MarketSummary


def format_filter_value(value: str | None) -> str:
    """Format report filter value.
    Args:
        value (str | None): Filter value.
    """
    if value is None or not value.strip():
        return 'all'

    return value.strip()


def build_analytics_report(
    analytics_run: AnalyticsRun,
    market_summary: MarketSummary | None,
    city: str | None,
    profile: str | None,
) -> str:
    """Build analytics report content.
    Args:
        analytics_run (AnalyticsRun): Analytics run model.
        market_summary (MarketSummary | None): Market summary model.
        city (str | None): City filter.
        profile (str | None): Profile filter.
    """
    report_lines = [
        '# Pipeline 2 Summary Analytics Report',
        '',
        '## Run information',
        '',
        f'- Analytics run ID: {analytics_run.id}',
        f'- Analytics name: {analytics_run.analytics_name}',
        f'- Client ID: {analytics_run.client_id}',
        f'- Date from: {analytics_run.date_from}',
        f'- Date to: {analytics_run.date_to}',
        f'- City filter: {format_filter_value(value=city)}',
        f'- Profile filter: {format_filter_value(value=profile)}',
        f'- Status: {analytics_run.status}',
        f'- Is success: {analytics_run.is_success}',
        f'- Snapshot count: {analytics_run.snapshot_count}',
        f'- Report name: {analytics_run.report_name}',
        f'- Created at: {analytics_run.created_at}',
        '',
    ]

    if market_summary is None:
        report_lines.extend(
            [
                '## Market summary',
                '',
                'Market summary was not created because input data is empty.',
                '',
            ],
        )

        return '\n'.join(report_lines)

    report_lines.extend(
        [
            '## Market summary',
            '',
            f'- Total snapshot count: '
            f'{market_summary.total_snapshot_count}',
            f'- Total company count: '
            f'{market_summary.total_company_count}',
            f'- Total vacancy count: '
            f'{market_summary.total_vacancy_count}',
            f'- Total callbacks: {market_summary.total_callbacks}',
            f'- Average callbacks: {market_summary.avg_callbacks}',
            f'- Median callbacks: {market_summary.median_callbacks}',
            f'- Mode city: {market_summary.mode_city}',
            f'- Mode region: {market_summary.mode_region}',
            f'- Mode profile: {market_summary.mode_profile}',
            f'- Mode tariff: {market_summary.mode_tariff}',
            f'- Mode work schedule: '
            f'{market_summary.mode_work_schedule}',
            f'- Mode work experience: '
            f'{market_summary.mode_work_experience}',
            f'- Mode employment type: '
            f'{market_summary.mode_employment_type}',
            f'- Median salary from: '
            f'{market_summary.median_salary_from}',
            f'- Median salary to: {market_summary.median_salary_to}',
            f'- Salary specified share: '
            f'{market_summary.salary_specified_share}',
            f'- Salary missing share: '
            f'{market_summary.salary_missing_share}',
            '',
        ],
    )

    return '\n'.join(report_lines)
