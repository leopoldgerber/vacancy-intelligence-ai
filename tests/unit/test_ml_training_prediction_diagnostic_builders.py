import pandas as pd

from app.services.ml_training.prediction_diagnostic_builders import (
    build_group_errors,
)
from app.services.ml_training.prediction_diagnostic_builders import (
    build_prediction_diagnostics,
)
from app.services.ml_training.prediction_diagnostic_builders import (
    build_worst_predictions,
)
from app.services.ml_training.prediction_diagnostic_builders import (
    enrich_prediction_data,
)


def build_prediction_rows() -> list[dict[str, object]]:
    """Build prediction rows for diagnostics tests.
    Args:
        """
    return [
        {
            'ml_training_run_id': 1,
            'source_row_index': 0,
            'client_id': 1,
            'company_id': 57,
            'vacancy_id': 17,
            'date_day': pd.Timestamp('2025-08-20'),
            'split_name': 'test',
            'target_name': 'callbacks',
            'actual_value': 3.0,
            'predicted_value': 4.5,
            'prediction_error': 1.5,
            'absolute_error': 1.5,
            'squared_error': 2.25,
        },
        {
            'ml_training_run_id': 1,
            'source_row_index': 1,
            'client_id': 1,
            'company_id': 58,
            'vacancy_id': 18,
            'date_day': pd.Timestamp('2025-09-03'),
            'split_name': 'test',
            'target_name': 'callbacks',
            'actual_value': 7.0,
            'predicted_value': 5.0,
            'prediction_error': -2.0,
            'absolute_error': 2.0,
            'squared_error': 4.0,
        },
        {
            'ml_training_run_id': 1,
            'source_row_index': 2,
            'client_id': 1,
            'company_id': 57,
            'vacancy_id': 19,
            'date_day': pd.Timestamp('2025-09-10'),
            'split_name': 'test',
            'target_name': 'callbacks',
            'actual_value': 2.0,
            'predicted_value': 2.5,
            'prediction_error': 0.5,
            'absolute_error': 0.5,
            'squared_error': 0.25,
        },
    ]


def build_source_data() -> pd.DataFrame:
    """Build source data for diagnostics tests.
    Args:
        """
    return pd.DataFrame(
        [
            {
                'profile': 'Verkäufer',
                'city': 'Berlin',
                'company_id': 57,
            },
            {
                'profile': 'Filialleiter',
                'city': 'Hamburg',
                'company_id': 58,
            },
            {
                'profile': 'Verkäufer',
                'city': 'Berlin',
                'company_id': 57,
            },
        ],
    )


def test_enrich_prediction_data() -> None:
    """Test prediction data enrichment.
    Args:
        """
    prediction_rows = build_prediction_rows()
    source_data = build_source_data()

    result = enrich_prediction_data(
        prediction_rows=prediction_rows,
        source_data=source_data,
    )

    assert len(result) == 3
    assert 'profile' in result.columns
    assert 'city' in result.columns
    assert result.loc[0, 'profile'] == 'Verkäufer'
    assert result.loc[1, 'profile'] == 'Filialleiter'
    assert result.loc[2, 'city'] == 'Berlin'


def test_build_group_errors() -> None:
    """Test group error builder.
    Args:
        """
    prediction_rows = build_prediction_rows()
    source_data = build_source_data()
    prediction_data = enrich_prediction_data(
        prediction_rows=prediction_rows,
        source_data=source_data,
    )

    result = build_group_errors(
        prediction_data=prediction_data,
        group_column='profile',
    )

    assert result == {
        'Filialleiter': 2.0,
        'Verkäufer': 1.0,
    }


def test_build_group_errors_missing_column() -> None:
    """Test group error builder with missing column.
    Args:
        """
    prediction_rows = build_prediction_rows()
    prediction_data = pd.DataFrame(prediction_rows)

    result = build_group_errors(
        prediction_data=prediction_data,
        group_column='profile',
    )

    assert result == {}


def test_build_worst_predictions() -> None:
    """Test worst prediction builder.
    Args:
        """
    prediction_rows = build_prediction_rows()
    source_data = build_source_data()
    prediction_data = enrich_prediction_data(
        prediction_rows=prediction_rows,
        source_data=source_data,
    )

    result = build_worst_predictions(
        prediction_data=prediction_data,
        top_row_count=2,
    )

    assert len(result) == 2
    assert result[0]['vacancy_id'] == 18
    assert result[0]['absolute_error'] == 2.0
    assert result[1]['vacancy_id'] == 17
    assert result[1]['absolute_error'] == 1.5


def test_build_prediction_diagnostics() -> None:
    """Test prediction diagnostics builder.
    Args:
        """
    prediction_rows = build_prediction_rows()
    source_data = build_source_data()

    result = build_prediction_diagnostics(
        prediction_rows=prediction_rows,
        source_data=source_data,
    )

    assert result['prediction_row_count'] == 3
    assert result['mean_prediction_error'] == 0.0
    assert result['mean_absolute_error'] == 1.3333333333333333
    assert result['max_absolute_error'] == 2.0
    assert result['mean_squared_error'] == 2.1666666666666665
    assert result['root_mean_squared_error'] == 1.4719601443879744
    assert result['over_prediction_count'] == 2
    assert result['under_prediction_count'] == 1
    assert result['mean_absolute_error_by_profile'] == {
        'Filialleiter': 2.0,
        'Verkäufer': 1.0,
    }
    assert result['mean_absolute_error_by_city'] == {
        'Hamburg': 2.0,
        'Berlin': 1.0,
    }
    assert result['mean_absolute_error_by_company_id'] == {
        '58': 2.0,
        '57': 1.0,
    }
    assert len(result['top_worst_predictions']) == 3
    assert result['top_worst_predictions'][0]['vacancy_id'] == 18


def test_build_prediction_diagnostics_empty() -> None:
    """Test empty prediction diagnostics builder.
    Args:
        """
    result = build_prediction_diagnostics(
        prediction_rows=[],
        source_data=pd.DataFrame(),
    )

    assert result == {
        'prediction_row_count': 0,
        'mean_prediction_error': None,
        'mean_absolute_error': None,
        'max_absolute_error': None,
        'mean_squared_error': None,
        'root_mean_squared_error': None,
        'over_prediction_count': 0,
        'under_prediction_count': 0,
        'mean_absolute_error_by_profile': {},
        'mean_absolute_error_by_city': {},
        'mean_absolute_error_by_company_id': {},
        'top_worst_predictions': [],
    }
