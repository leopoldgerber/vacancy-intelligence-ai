from datetime import datetime

from app.db.models.vacancy import Vacancy


def create_vacancy(
    vacancy_id: int,
    client_id: int,
    company_id: int,
    vacancy_title: str,
    vacancy_description: str,
    employment_type: str | None,
    profile: str,
    publication_date: datetime,
    region: str,
    city: str,
    salary_from: int | None,
    salary_to: int | None,
    tariff: str | None,
    work_experience: str | None,
    work_schedule: str | None,
    standard: int,
    standard_plus: int,
    premium: int,
) -> Vacancy:
    """Create vacancy model instance.
    Args:
        vacancy_id (int): Vacancy identifier.
        client_id (int): Client identifier.
        company_id (int): Company identifier.
        vacancy_title (str): Vacancy title.
        vacancy_description (str): Vacancy description.
        employment_type (str | None): Employment type.
        profile (str): Vacancy profile.
        publication_date (datetime): Publication datetime.
        region (str): Region name.
        city (str): City name.
        salary_from (int | None): Salary lower bound.
        salary_to (int | None): Salary upper bound.
        tariff (str | None): Tariff name.
        work_experience (str | None): Work experience.
        work_schedule (str | None): Work schedule.
        standard (int): Standard flag.
        standard_plus (int): Standard plus flag.
        premium (int): Premium flag."""
    vacancy = Vacancy(
        vacancy_id=vacancy_id,
        client_id=client_id,
        company_id=company_id,
        vacancy_title=vacancy_title,
        vacancy_description=vacancy_description,
        employment_type=employment_type,
        profile=profile,
        publication_date=publication_date,
        region=region,
        city=city,
        salary_from=salary_from,
        salary_to=salary_to,
        tariff=tariff,
        work_experience=work_experience,
        work_schedule=work_schedule,
        standard=standard,
        standard_plus=standard_plus,
        premium=premium,
    )
    return vacancy


def update_vacancy(
    vacancy: Vacancy,
    client_id: int,
    company_id: int,
    vacancy_title: str,
    vacancy_description: str,
    employment_type: str | None,
    profile: str,
    publication_date: datetime,
    region: str,
    city: str,
    salary_from: int | None,
    salary_to: int | None,
    tariff: str | None,
    work_experience: str | None,
    work_schedule: str | None,
    standard: int,
    standard_plus: int,
    premium: int,
) -> Vacancy:
    """Update vacancy model instance.
    Args:
        vacancy (Vacancy): Vacancy model instance.
        client_id (int): Client identifier.
        company_id (int): Company identifier.
        vacancy_title (str): Vacancy title.
        vacancy_description (str): Vacancy description.
        employment_type (str | None): Employment type.
        profile (str): Vacancy profile.
        publication_date (datetime): Publication datetime.
        region (str): Region name.
        city (str): City name.
        salary_from (int | None): Salary lower bound.
        salary_to (int | None): Salary upper bound.
        tariff (str | None): Tariff name.
        work_experience (str | None): Work experience.
        work_schedule (str | None): Work schedule.
        standard (int): Standard flag.
        standard_plus (int): Standard plus flag.
        premium (int): Premium flag."""
    vacancy.client_id = client_id
    vacancy.company_id = company_id
    vacancy.vacancy_title = vacancy_title
    vacancy.vacancy_description = vacancy_description
    vacancy.employment_type = employment_type
    vacancy.profile = profile
    vacancy.publication_date = publication_date
    vacancy.region = region
    vacancy.city = city
    vacancy.salary_from = salary_from
    vacancy.salary_to = salary_to
    vacancy.tariff = tariff
    vacancy.work_experience = work_experience
    vacancy.work_schedule = work_schedule
    vacancy.standard = standard
    vacancy.standard_plus = standard_plus
    vacancy.premium = premium

    return vacancy
