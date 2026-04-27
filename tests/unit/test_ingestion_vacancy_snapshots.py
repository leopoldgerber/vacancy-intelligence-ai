from datetime import datetime

from app.services.ingestion.vacancy_snapshots.service import build_snapshot_key


def test_build_snapshot_key_from_string_date() -> None:
    """Test snapshot key builder from string date.
    Args:
        """
    result = build_snapshot_key(
        client_id=1,
        company_id=2,
        vacancy_id=3,
        date_day='2025-08-04 00:00:00',
    )

    assert result == (
        1,
        2,
        3,
        datetime(2025, 8, 4, 0, 0, 0),
    )


def test_build_snapshot_key_from_datetime() -> None:
    """Test snapshot key builder from datetime value.
    Args:
        """
    result = build_snapshot_key(
        client_id=1,
        company_id=2,
        vacancy_id=3,
        date_day=datetime(2025, 8, 4, 0, 0, 0),
    )

    assert result == (
        1,
        2,
        3,
        datetime(2025, 8, 4, 0, 0, 0),
    )
