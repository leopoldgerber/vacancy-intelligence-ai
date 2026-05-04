import pandas as pd
import pytest

from app.services.features.salary_feature_builders import (
    build_salary_feature_dataframe,
)
from app.services.features.salary_feature_builders import (
    build_salary_feature_rows,
)
from app.services.features.salary_feature_builders import (
    calculate_salary_mid,
)
from app.services.features.salary_feature_builders import (
    calculate_salary_ratio,
)


def build_salary_dataframe() -> pd.DataFrame:
    """Build salary feature test dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1, 1, 1, 1, 1, 1],
            'company_id': [10, 10, 20, 20, 30, 30],
            'vacancy_id': [100, 101, 200, 201, 300, 301],
            'date_day': pd.to_datetime(
                [
                    '2025-08-01',
                    '2025-08-01',
                    '2025-08-01',
                    '2025-08-01',
                    '2025-08-01',
                    '2025-08-01',
                ],
            ),
            'city': [
                'Berlin',
                'Berlin',
                'Berlin',
                'Berlin',
                'Berlin',
                'Berlin',
            ],
            'profile': [
                'Filialleiter',
                'Filialleiter',
                'Filialleiter',
                'Filialleiter',
                'Filialleiter',
                'Filialleiter',
            ],
            'salary_from': [
                1000.0,
                1200.0,
                2000.0,
                2200.0,
                3000.0,
                None,
            ],
            'salary_to': [
                2000.0,
                2400.0,
                4000.0,
                4400.0,
                None,
                3600.0,
            ],
        },
    )


def test_calculate_salary_mid_with_both_bounds() -> None:
    """Test salary midpoint with both salary bounds.
    Args:
        """
    result = calculate_salary_mid(
        salary_from=1000.0,
        salary_to=2000.0,
    )

    assert result == 1500.0


def test_calculate_salary_mid_with_only_salary_from() -> None:
    """Test salary midpoint with only salary_from.
    Args:
        """
    result = calculate_salary_mid(
        salary_from=3000.0,
        salary_to=None,
    )

    assert result == 3000.0


def test_calculate_salary_mid_with_only_salary_to() -> None:
    """Test salary midpoint with only salary_to.
    Args:
        """
    result = calculate_salary_mid(
        salary_from=None,
        salary_to=3600.0,
    )

    assert result == 3600.0


def test_calculate_salary_mid_without_salary() -> None:
    """Test salary midpoint without salary values.
    Args:
        """
    result = calculate_salary_mid(
        salary_from=None,
        salary_to=None,
    )

    assert result == 0.0


def test_calculate_salary_ratio() -> None:
    """Test salary ratio calculation.
    Args:
        """
    result = calculate_salary_ratio(
        company_salary_median=1500.0,
        market_salary_median=3000.0,
    )

    assert result == 0.5


def test_calculate_salary_ratio_with_zero_market() -> None:
    """Test salary ratio when market median is zero.
    Args:
        """
    result = calculate_salary_ratio(
        company_salary_median=1500.0,
        market_salary_median=0.0,
    )

    assert result == 0.0


def test_build_salary_feature_dataframe() -> None:
    """Test salary feature dataframe builder.
    Args:
        """
    data = build_salary_dataframe()

    result = build_salary_feature_dataframe(data=data)

    assert len(result) == 6

    company_10_rows = result[result['company_id'] == 10]
    company_20_rows = result[result['company_id'] == 20]
    company_30_rows = result[result['company_id'] == 30]

    assert company_10_rows['salary_mid'].tolist() == [1500.0, 1800.0]
    assert company_20_rows['salary_mid'].tolist() == [3000.0, 3300.0]
    assert company_30_rows['salary_mid'].tolist() == [3000.0, 3600.0]

    assert company_10_rows[
        'company_salary_median_by_city'
    ].iloc[0] == 1650.0
    assert company_20_rows[
        'company_salary_median_by_city'
    ].iloc[0] == 3150.0
    assert company_30_rows[
        'company_salary_median_by_city'
    ].iloc[0] == 3300.0

    assert company_10_rows[
        'market_salary_median_excl_company_by_city'
    ].iloc[0] == 3150.0
    assert company_20_rows[
        'market_salary_median_excl_company_by_city'
    ].iloc[0] == 2400.0
    assert company_30_rows[
        'market_salary_median_excl_company_by_city'
    ].iloc[0] == 2400.0

    assert company_10_rows[
        'salary_ratio_to_market_by_city'
    ].iloc[0] == pytest.approx(1650.0 / 3150.0)
    assert company_20_rows[
        'salary_ratio_to_market_by_city'
    ].iloc[0] == pytest.approx(3150.0 / 2400.0)
    assert company_30_rows[
        'salary_ratio_to_market_by_city'
    ].iloc[0] == pytest.approx(3300.0 / 2400.0)

    assert company_10_rows[
        'salary_ratio_to_market_by_profile'
    ].iloc[0] == pytest.approx(1650.0 / 3150.0)
    assert company_10_rows[
        'salary_ratio_to_market_by_city_profile'
    ].iloc[0] == pytest.approx(1650.0 / 3150.0)


def test_build_salary_feature_dataframe_empty_data() -> None:
    """Test salary feature dataframe builder with empty data.
    Args:
        """
    data = pd.DataFrame()

    result = build_salary_feature_dataframe(data=data)

    assert result.empty


def test_build_salary_feature_rows() -> None:
    """Test salary feature rows builder.
    Args:
        """
    data = build_salary_dataframe()

    result = build_salary_feature_rows(
        data=data,
        feature_run_id=1,
    )

    assert len(result) == 6

    first_row = result[0]

    assert first_row['feature_run_id'] == 1
    assert first_row['client_id'] == 1
    assert first_row['company_id'] == 10
    assert first_row['vacancy_id'] == 100
    assert first_row['salary_mid'] == 1500.0
    assert first_row['salary_is_specified'] is True
    assert first_row['company_salary_median_by_city'] == 1650.0
    assert first_row[
        'market_salary_median_excl_company_by_city'
    ] == 3150.0
    assert first_row[
        'salary_ratio_to_market_by_city'
    ] == pytest.approx(1650.0 / 3150.0)


def test_build_salary_feature_rows_empty_data() -> None:
    """Test salary feature rows builder with empty data.
    Args:
        """
    data = pd.DataFrame()

    result = build_salary_feature_rows(
        data=data,
        feature_run_id=1,
    )

    assert result == []
