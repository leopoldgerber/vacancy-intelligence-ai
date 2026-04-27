from app.db.models.vacancy import Vacancy
from app.services.ingestion.vacancies.service import (
    build_vacancy_id_map,
    build_vacancy_map,
)


def build_vacancies() -> list[Vacancy]:
    """Build vacancy model instances for tests.
    Args:
        """
    vacancies = [
        Vacancy(
            vacancy_id=1,
            client_id=1,
            company_id=1,
            vacancy_title='Vacancy 1',
            vacancy_description='Description 1',
            employment_type='Full-time',
            profile='Seller',
            publication_date='2025-08-04 13:09:25',
            region='Sachsen',
            city='Leipzig',
            salary_from=15,
            salary_to=17,
            tariff='Premium',
            work_experience='No experience required',
            work_schedule='Shift work',
            standard=0,
            standard_plus=0,
            premium=1,
        ),
        Vacancy(
            vacancy_id=2,
            client_id=1,
            company_id=2,
            vacancy_title='Vacancy 2',
            vacancy_description='Description 2',
            employment_type='Part-time',
            profile='Seller',
            publication_date='2025-08-05 11:30:00',
            region='Berlin',
            city='Berlin',
            salary_from=16,
            salary_to=18,
            tariff='Standard Plus',
            work_experience='No experience required',
            work_schedule='Shift work',
            standard=0,
            standard_plus=1,
            premium=0,
        ),
    ]
    return vacancies


def test_build_vacancy_map() -> None:
    """Test vacancy model map builder.
    Args:
        """
    vacancies = build_vacancies()

    result = build_vacancy_map(vacancies=vacancies)

    assert result == {
        1: vacancies[0],
        2: vacancies[1],
    }


def test_build_vacancy_id_map() -> None:
    """Test vacancy identifier map builder.
    Args:
        """
    vacancies = build_vacancies()

    result = build_vacancy_id_map(vacancies=vacancies)

    assert result == {
        1: 1,
        2: 2,
    }
