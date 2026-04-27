import pandas as pd

from app.services.data_quality.result_builders import (
    build_quality_issue_data,
    build_quality_result,
    build_quality_run_data,
    build_warning_count,
)


def build_test_dataframe() -> pd.DataFrame:
    """Build dataframe for quality result builder tests.
    Args:
        """
    data = pd.DataFrame(
        {
            'client_id': [1, 1, 1],
            'company_name': ['company_1', 'company_2', 'company_3'],
            'vacancy_id': [101, 102, 103],
        }
    )
    return data


def build_quality_results() -> dict[str, dict[str, int | str]]:
    """Build quality check results.
    Args:
        """
    quality_results = {
        'sample': {
            'row_count': 3,
            'column_count': 3,
        },
        'missing_values': {
            'rule_name': 'missing_values_check',
            'issue_count': 2,
            'message': 'Dataset contains missing values.',
        },
        'duplicate_rows': {
            'rule_name': 'duplicate_rows_check',
            'issue_count': 1,
            'message': 'Dataset contains duplicate rows.',
        },
        'empty_text_values': {
            'rule_name': 'empty_text_values_check',
            'issue_count': 4,
            'message': 'Text columns contain empty values.',
        },
        'whitespace_text_values': {
            'rule_name': 'whitespace_text_values_check',
            'issue_count': 3,
            'message': 'Text columns contain whitespace-only values.',
        },
    }
    return quality_results


def test_build_warning_count() -> None:
    """Test quality warning count builder.
    Args:
        """
    quality_results = build_quality_results()

    result = build_warning_count(quality_results=quality_results)

    assert result == 10


def test_build_quality_issue_data() -> None:
    """Test quality issue data builder.
    Args:
        """
    quality_results = build_quality_results()

    result = build_quality_issue_data(quality_results=quality_results)

    assert result == {
        'missing_values_count': 2,
        'duplicate_row_count': 1,
        'empty_text_values_count': 4,
        'whitespace_text_values_count': 3,
    }


def test_build_quality_run_data() -> None:
    """Test quality run data builder.
    Args:
        """
    data = build_test_dataframe()

    result = build_quality_run_data(
        data=data,
        quality_name='quality_2026-04-27_10-39-15',
        source_name='input.xlsx',
        report_name='quality_2026-04-27_10-39-15.md',
        warning_count=10,
    )

    assert result == {
        'quality_name': 'quality_2026-04-27_10-39-15',
        'source_name': 'input.xlsx',
        'warning_count': 10,
        'report_name': 'quality_2026-04-27_10-39-15.md',
    }


def test_build_quality_result() -> None:
    """Test final quality result builder.
    Args:
        """
    data = build_test_dataframe()
    quality_results = build_quality_results()

    result = build_quality_result(
        data=data,
        quality_name='quality_test',
        source_name='input.xlsx',
        report_name='quality_test.md',
        quality_results=quality_results,
    )

    assert result['quality_run']['quality_name'] == 'quality_test'
    assert result['quality_run']['source_name'] == 'input.xlsx'
    assert result['quality_run']['warning_count'] == 10
    assert result['quality_run']['report_name'] == 'quality_test.md'
    assert result['quality_issue']['missing_values_count'] == 2
    assert result['quality_issue']['duplicate_row_count'] == 1
    assert result['quality_issue']['empty_text_values_count'] == 4
    assert result['quality_issue']['whitespace_text_values_count'] == 3
