from datetime import datetime

import pandas as pd

from app.services.features.text_feature_builders import (
    build_text_feature_dataframe,
)
from app.services.features.text_feature_builders import (
    build_text_feature_rows,
)
from app.services.features.text_feature_builders import clean_text
from app.services.features.text_feature_builders import contains_keyword
from app.services.features.text_feature_builders import count_words


def build_text_feature_test_dataframe() -> pd.DataFrame:
    """Build text feature test dataframe.
    Args:
        """
    return pd.DataFrame(
        {
            'client_id': [1, 1, 1],
            'company_id': [10, 10, 20],
            'vacancy_id': [100, 101, 200],
            'date_day': pd.to_datetime(
                [
                    '2025-08-01',
                    '2025-08-01',
                    '2025-08-01',
                ],
            ),
            'vacancy_title': [
                'Filialleiter Vollzeit',
                'Aushilfe',
                None,
            ],
            'vacancy_description': [
                (
                    'Wir bieten Gehalt, Weiterbildung und flexible '
                    'Arbeitszeit. Du bringst Erfahrung mit. '
                    'Bewirb dich jetzt.'
                ),
                '',
                None,
            ],
        },
    )


def test_clean_text() -> None:
    """Test text cleaning.
    Args:
        """
    result = clean_text(value='  Hallo    Welt \n Test  ')

    assert result == 'Hallo Welt Test'


def test_clean_text_none() -> None:
    """Test text cleaning with None.
    Args:
        """
    result = clean_text(value=None)

    assert result == ''


def test_count_words() -> None:
    """Test word count.
    Args:
        """
    result = count_words(value='Filialleiter Vollzeit Berlin')

    assert result == 3


def test_count_words_empty_text() -> None:
    """Test word count with empty text.
    Args:
        """
    result = count_words(value='   ')

    assert result == 0


def test_contains_keyword() -> None:
    """Test keyword detection.
    Args:
        """
    result = contains_keyword(
        text='Wir bieten ein attraktives Gehalt.',
        keywords=['gehalt'],
    )

    assert result is True


def test_contains_keyword_false() -> None:
    """Test keyword detection without matching keyword.
    Args:
        """
    result = contains_keyword(
        text='Wir suchen Verstärkung.',
        keywords=['gehalt'],
    )

    assert result is False


def test_build_text_feature_dataframe() -> None:
    """Test text feature dataframe builder.
    Args:
        """
    data = build_text_feature_test_dataframe()

    result = build_text_feature_dataframe(data=data)

    assert len(result) == 3

    first_row = result.iloc[0]
    second_row = result.iloc[1]
    third_row = result.iloc[2]

    assert first_row['title_length'] == len('Filialleiter Vollzeit')
    assert first_row['description_length'] > 0
    assert first_row['title_word_count'] == 2
    assert first_row['description_word_count'] > 0
    assert bool(first_row['has_description']) is True
    assert bool(first_row['description_is_empty']) is False
    assert bool(first_row['has_salary_mention']) is True
    assert bool(first_row['has_schedule_mention']) is True
    assert bool(first_row['has_requirements_mention']) is True
    assert bool(first_row['has_benefits_mention']) is True
    assert bool(first_row['has_call_to_action']) is True

    assert second_row['title_length'] == len('Aushilfe')
    assert second_row['description_length'] == 0
    assert second_row['title_word_count'] == 1
    assert second_row['description_word_count'] == 0
    assert bool(second_row['has_description']) is False
    assert bool(second_row['description_is_empty']) is True
    assert bool(second_row['has_salary_mention']) is False

    assert third_row['title_length'] == 0
    assert third_row['description_length'] == 0
    assert third_row['title_word_count'] == 0
    assert third_row['description_word_count'] == 0
    assert bool(third_row['has_description']) is False
    assert bool(third_row['description_is_empty']) is True


def test_build_text_feature_dataframe_empty_data() -> None:
    """Test text feature dataframe builder with empty data.
    Args:
        """
    data = pd.DataFrame()

    result = build_text_feature_dataframe(data=data)

    assert result.empty


def test_build_text_feature_rows() -> None:
    """Test text feature rows builder.
    Args:
        """
    data = build_text_feature_test_dataframe()

    result = build_text_feature_rows(
        data=data,
        feature_run_id=1,
    )

    assert len(result) == 3

    first_row = result[0]

    assert first_row['feature_run_id'] == 1
    assert first_row['client_id'] == 1
    assert first_row['company_id'] == 10
    assert first_row['vacancy_id'] == 100
    assert isinstance(first_row['date_day'], pd.Timestamp | datetime)
    assert first_row['title_length'] == len('Filialleiter Vollzeit')
    assert first_row['title_word_count'] == 2
    assert first_row['has_description'] is True
    assert first_row['description_is_empty'] is False
    assert first_row['has_salary_mention'] is True
    assert first_row['has_schedule_mention'] is True
    assert first_row['has_requirements_mention'] is True
    assert first_row['has_benefits_mention'] is True
    assert first_row['has_call_to_action'] is True


def test_build_text_feature_rows_empty_data() -> None:
    """Test text feature rows builder with empty data.
    Args:
        """
    data = pd.DataFrame()

    result = build_text_feature_rows(
        data=data,
        feature_run_id=1,
    )

    assert result == []
