from datetime import datetime

import pandas as pd

from app.services.ingestion.vacancies.service import parse_datetime_value
from app.services.ingestion.vacancies.service import parse_nullable_integer
from app.services.ingestion.vacancies.service import parse_nullable_string


def test_parse_datetime_value_from_string() -> None:
    """Test datetime parsing from string.
    Args:
        """
    result = parse_datetime_value(value='2025-08-04 13:09:25')

    assert result == datetime(2025, 8, 4, 13, 9, 25)


def test_parse_datetime_value_from_timestamp() -> None:
    """Test datetime parsing from pandas timestamp.
    Args:
        """
    value = pd.Timestamp('2025-08-04 13:09:25')

    result = parse_datetime_value(value=value)

    assert result == datetime(2025, 8, 4, 13, 9, 25)


def test_parse_nullable_string_from_text() -> None:
    """Test nullable string parsing from text.
    Args:
        """
    result = parse_nullable_string(value='Premium')

    assert result == 'Premium'


def test_parse_nullable_string_from_empty_string() -> None:
    """Test nullable string parsing from empty string.
    Args:
        """
    result = parse_nullable_string(value='')

    assert result is None


def test_parse_nullable_string_from_whitespace() -> None:
    """Test nullable string parsing from whitespace.
    Args:
        """
    result = parse_nullable_string(value='   ')

    assert result is None


def test_parse_nullable_string_from_none() -> None:
    """Test nullable string parsing from None.
    Args:
        """
    result = parse_nullable_string(value=None)

    assert result is None


def test_parse_nullable_string_from_nan() -> None:
    """Test nullable string parsing from NaN.
    Args:
        """
    result = parse_nullable_string(value=float('nan'))

    assert result is None


def test_parse_nullable_integer_from_integer() -> None:
    """Test nullable integer parsing from integer.
    Args:
        """
    result = parse_nullable_integer(value=15)

    assert result == 15


def test_parse_nullable_integer_from_float_integer() -> None:
    """Test nullable integer parsing from float integer.
    Args:
        """
    result = parse_nullable_integer(value=15.0)

    assert result == 15


def test_parse_nullable_integer_from_string_integer() -> None:
    """Test nullable integer parsing from string integer.
    Args:
        """
    result = parse_nullable_integer(value='15')

    assert result == 15


def test_parse_nullable_integer_from_none() -> None:
    """Test nullable integer parsing from None.
    Args:
        """
    result = parse_nullable_integer(value=None)

    assert result is None


def test_parse_nullable_integer_from_nan() -> None:
    """Test nullable integer parsing from NaN.
    Args:
        """
    result = parse_nullable_integer(value=float('nan'))

    assert result is None
