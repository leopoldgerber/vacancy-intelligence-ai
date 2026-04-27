from datetime import datetime

from app.db.models.vacancy_snapshot import VacancySnapshot


def create_vacancy_snapshot(
    client_id: int,
    company_id: int,
    vacancy_id: int,
    date_day: datetime,
    publication_date: datetime,
    vacancy_title: str,
    vacancy_description: str,
    employment_type: str | None,
    profile: str,
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
    callbacks: int,
) -> VacancySnapshot:
    """Create vacancy snapshot model instance.
    Args:
        client_id (int): Client identifier.
        company_id (int): Company identifier.
        vacancy_id (int): Vacancy identifier.
        date_day (datetime): Snapshot date.
        publication_date (datetime): Publication datetime.
        vacancy_title (str): Vacancy title.
        vacancy_description (str): Vacancy description.
        employment_type (str | None): Employment type.
        profile (str): Vacancy profile.
        region (str): Region name.
        city (str): City name.
        salary_from (int | None): Salary lower bound.
        salary_to (int | None): Salary upper bound.
        tariff (str | None): Tariff name.
        work_experience (str | None): Work experience.
        work_schedule (str | None): Work schedule.
        standard (int): Standard flag.
        standard_plus (int): Standard plus flag.
        premium (int): Premium flag.
        callbacks (int): Callbacks count."""
    vacancy_snapshot = VacancySnapshot(
        client_id=client_id,
        company_id=company_id,
        vacancy_id=vacancy_id,
        date_day=date_day,
        publication_date=publication_date,
        vacancy_title=vacancy_title,
        vacancy_description=vacancy_description,
        employment_type=employment_type,
        profile=profile,
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
        callbacks=callbacks,
    )
    return vacancy_snapshot
