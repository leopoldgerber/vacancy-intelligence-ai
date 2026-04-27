import pandas as pd

from app.db.models.company import Company
from app.services.ingestion.companies.service import (
    build_company_map,
    build_company_pairs,
)


def build_company_dataframe() -> pd.DataFrame:
    """Build dataframe for company ingestion tests.
    Args:
        """
    data = pd.DataFrame(
        [
            {
                'client_id': 1,
                'company_name': 'company_1',
            },
            {
                'client_id': 1,
                'company_name': 'company_2',
            },
            {
                'client_id': 1,
                'company_name': 'company_1',
            },
            {
                'client_id': 2,
                'company_name': 'company_1',
            },
        ]
    )
    return data


def test_build_company_pairs() -> None:
    """Test company pair builder.
    Args:
        """
    data = build_company_dataframe()

    result = build_company_pairs(data=data)

    assert result == [
        (1, 'company_1'),
        (1, 'company_2'),
        (2, 'company_1'),
    ]


def test_build_company_map() -> None:
    """Test company identifier map builder.
    Args:
        """
    companies = [
        Company(
            id=1,
            client_id=1,
            name='company_1',
        ),
        Company(
            id=2,
            client_id=1,
            name='company_2',
        ),
        Company(
            id=3,
            client_id=2,
            name='company_1',
        ),
    ]

    result = build_company_map(companies=companies)

    assert result == {
        (1, 'company_1'): 1,
        (1, 'company_2'): 2,
        (2, 'company_1'): 3,
    }
