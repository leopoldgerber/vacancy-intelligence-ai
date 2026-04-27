from io import BytesIO

import pandas as pd


def build_test_dataframe() -> pd.DataFrame:
    """Build valid input dataframe for pipeline test.
    Args:
        """
    data = pd.DataFrame(
        [
            {
                'city': 'Leipzig',
                'client_id': 1,
                'company_name': 'company_1',
                'employment_type': 'Full-time',
                'date_day': '2025-08-04 00:00:00',
                'profile': 'Verkäufer',
                'publication_date': '2025-08-04 13:09:25',
                'region': 'Sachsen',
                'salary_from': 15,
                'salary_to': 17,
                'tariff': 'Premium',
                'vacancy_description': 'Valid vacancy description.',
                'vacancy_id': 1,
                'vacancy_title': 'Verkäufer / Kassierer Vollzeit',
                'work_experience': 'Quereinsteiger',
                'work_schedule': 'Schichtarbeit',
                'standard': 0,
                'standard_plus': 0,
                'premium': 1,
                'callbacks': 5,
            },
            {
                'city': 'Berlin',
                'client_id': 1,
                'company_name': 'company_2',
                'employment_type': 'Part-time',
                'date_day': '2025-08-05 00:00:00',
                'profile': 'Verkäufer',
                'publication_date': '2025-08-05 11:30:00',
                'region': 'Berlin',
                'salary_from': 16,
                'salary_to': 18,
                'tariff': 'Standard Plus',
                'vacancy_description': 'Another valid vacancy description.',
                'vacancy_id': 2,
                'vacancy_title': 'Verkäufer / Kassierer Teilzeit',
                'work_experience': 'Quereinsteiger',
                'work_schedule': 'Schichtarbeit',
                'standard': 0,
                'standard_plus': 1,
                'premium': 0,
                'callbacks': 3,
            },
        ]
    )
    return data


def build_xlsx_bytes(data: pd.DataFrame) -> bytes:
    """Build xlsx bytes from dataframe.
    Args:
        data (pd.DataFrame): Input dataframe."""
    buffer = BytesIO()
    data.to_excel(buffer, index=False)
    xlsx_bytes = buffer.getvalue()
    return xlsx_bytes
