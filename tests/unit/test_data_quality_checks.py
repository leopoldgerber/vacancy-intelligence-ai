import pandas as pd

from app.services.data_quality.checks import (
    build_text_columns,
    check_duplicate_rows,
    check_empty_text_values,
    check_missing_values,
    check_sample_size,
    check_whitespace_text_values,
    run_quality_checks,
)


def build_quality_dataframe() -> pd.DataFrame:
    """Build dataframe for quality checks.
    Args:
        """
    data = pd.DataFrame(
        [
            {
                'city': 'Leipzig',
                'company_name': 'company_1',
                'employment_type': 'Full-time',
                'profile': 'Verkäufer',
                'region': 'Sachsen',
                'tariff': 'Premium',
                'vacancy_description': 'Valid description.',
                'vacancy_title': 'Valid title',
                'work_experience': 'Quereinsteiger',
                'work_schedule': 'Schichtarbeit',
                'salary_from': 15,
            },
            {
                'city': '',
                'company_name': 'company_1',
                'employment_type': 'Full-time',
                'profile': 'Verkäufer',
                'region': 'Sachsen',
                'tariff': None,
                'vacancy_description': '   ',
                'vacancy_title': 'Valid title',
                'work_experience': 'Quereinsteiger',
                'work_schedule': 'Schichtarbeit',
                'salary_from': None,
            },
            {
                'city': '',
                'company_name': 'company_1',
                'employment_type': 'Full-time',
                'profile': 'Verkäufer',
                'region': 'Sachsen',
                'tariff': None,
                'vacancy_description': '   ',
                'vacancy_title': 'Valid title',
                'work_experience': 'Quereinsteiger',
                'work_schedule': 'Schichtarbeit',
                'salary_from': None,
            },
        ]
    )
    return data


def test_build_text_columns() -> None:
    """Test text column selection.
    Args:
        """
    data = build_quality_dataframe()

    result = build_text_columns(data=data)

    assert result == [
        'city',
        'company_name',
        'employment_type',
        'profile',
        'region',
        'tariff',
        'vacancy_description',
        'vacancy_title',
        'work_experience',
        'work_schedule',
    ]


def test_check_sample_size() -> None:
    """Test sample size check.
    Args:
        """
    data = build_quality_dataframe()

    result = check_sample_size(data=data)

    assert result == {
        'row_count': 3,
        'column_count': 11,
    }


def test_check_missing_values() -> None:
    """Test missing values check.
    Args:
        """
    data = build_quality_dataframe()

    result = check_missing_values(data=data)

    assert result['rule_name'] == 'missing_values_check'
    assert result['issue_count'] == 4
    assert result['message'] == 'Dataset contains missing values.'


def test_check_duplicate_rows() -> None:
    """Test duplicate rows check.
    Args:
        """
    data = build_quality_dataframe()

    result = check_duplicate_rows(data=data)

    assert result['rule_name'] == 'duplicate_rows_check'
    assert result['issue_count'] == 1
    assert result['message'] == 'Dataset contains duplicate rows.'


def test_check_empty_text_values() -> None:
    """Test empty text values check.
    Args:
        """
    data = build_quality_dataframe()
    text_columns = build_text_columns(data=data)

    result = check_empty_text_values(
        data=data,
        text_columns=text_columns,
    )

    assert result['rule_name'] == 'empty_text_values_check'
    assert result['issue_count'] == 4
    assert result['message'] == 'Text columns contain empty values.'


def test_check_whitespace_text_values() -> None:
    """Test whitespace-only text values check.
    Args:
        """
    data = build_quality_dataframe()
    text_columns = build_text_columns(data=data)

    result = check_whitespace_text_values(
        data=data,
        text_columns=text_columns,
    )

    assert result['rule_name'] == 'whitespace_text_values_check'
    assert result['issue_count'] == 2
    assert result['message'] == (
        'Text columns contain whitespace-only values.'
    )


def test_run_quality_checks() -> None:
    """Test full quality checks execution.
    Args:
        """
    data = build_quality_dataframe()

    result = run_quality_checks(data=data)

    assert 'sample' in result
    assert 'missing_values' in result
    assert 'duplicate_rows' in result
    assert 'empty_text_values' in result
    assert 'whitespace_text_values' in result

    assert result['sample']['row_count'] == 3
    assert result['sample']['column_count'] == 11
    assert result['missing_values']['issue_count'] == 4
    assert result['duplicate_rows']['issue_count'] == 1
    assert result['empty_text_values']['issue_count'] == 4
    assert result['whitespace_text_values']['issue_count'] == 2
