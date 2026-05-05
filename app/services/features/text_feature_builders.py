import re
from datetime import datetime

import pandas as pd


SALARY_KEYWORDS = [
    'salary',
    'gehalt',
    'vergütung',
    'lohn',
    'euro',
    '€',
    'brutto',
    'netto',
    'stundenlohn',
    'jahresgehalt',
    'monatsgehalt',
]

SCHEDULE_KEYWORDS = [
    'vollzeit',
    'teilzeit',
    'schicht',
    'schichtdienst',
    'arbeitszeit',
    'wochenende',
    'nachtschicht',
    'frühschicht',
    'spätschicht',
    'flexibel',
    'remote',
    'homeoffice',
    'hybrid',
]

REQUIREMENTS_KEYWORDS = [
    'anforderungen',
    'voraussetzungen',
    'erfahrung',
    'kenntnisse',
    'qualifikation',
    'ausbildung',
    'studium',
    'führerschein',
    'skills',
    'profil',
    'du bringst mit',
    'sie bringen mit',
]

BENEFITS_KEYWORDS = [
    'benefits',
    'vorteile',
    'wir bieten',
    'angebot',
    'rabatt',
    'bonus',
    'prämie',
    'urlaub',
    'weiterbildung',
    'entwicklung',
    'karriere',
    'team',
    'betriebliche altersvorsorge',
    'mitarbeiterrabatt',
]

CALL_TO_ACTION_KEYWORDS = [
    'bewirb dich',
    'bewerben sie sich',
    'jetzt bewerben',
    'apply now',
    'werde teil',
    'komm in unser team',
    'sende deine bewerbung',
    'wir freuen uns auf deine bewerbung',
]


def clean_text(value: str | None) -> str:
    """Clean text value.
    Args:
        value (str | None): Raw text value.
    """
    if value is None:
        return ''

    cleaned_value = str(value).strip()
    cleaned_value = re.sub(r'\s+', ' ', cleaned_value)

    return cleaned_value


def count_words(value: str | None) -> int:
    """Count words in text.
    Args:
        value (str | None): Text value.
    """
    cleaned_value = clean_text(value=value)

    if not cleaned_value:
        return 0

    return len(cleaned_value.split())


def contains_keyword(
    text: str,
    keywords: list[str],
) -> bool:
    """Check whether text contains at least one keyword.
    Args:
        text (str): Text to search in.
        keywords (list[str]): Keyword list.
    """
    normalized_text = clean_text(value=text).lower()

    if not normalized_text:
        return False

    return any(keyword.lower() in normalized_text for keyword in keywords)


def combine_title_and_description(
    title: str | None,
    description: str | None,
) -> str:
    """Combine title and description for keyword search.
    Args:
        title (str | None): Vacancy title.
        description (str | None): Vacancy description.
    """
    cleaned_title = clean_text(value=title)
    cleaned_description = clean_text(value=description)

    return f'{cleaned_title} {cleaned_description}'.strip()


def build_text_feature_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """Build text feature dataframe.
    Args:
        data (pd.DataFrame): Input snapshot dataframe.
    """
    if data.empty:
        return pd.DataFrame()

    feature_data = data.copy()

    feature_data['cleaned_title'] = feature_data['vacancy_title'].apply(
        clean_text,
    )
    feature_data['cleaned_description'] = feature_data[
        'vacancy_description'
    ].apply(clean_text)

    feature_data['title_length'] = feature_data['cleaned_title'].apply(len)
    feature_data['description_length'] = feature_data[
        'cleaned_description'
    ].apply(len)

    feature_data['title_word_count'] = feature_data['cleaned_title'].apply(
        count_words,
    )
    feature_data['description_word_count'] = feature_data[
        'cleaned_description'
    ].apply(count_words)

    feature_data['has_description'] = (
        feature_data['description_length'] > 0
    )
    feature_data['description_is_empty'] = (
        feature_data['description_length'] == 0
    )

    feature_data['combined_text'] = feature_data.apply(
        lambda row: combine_title_and_description(
            title=row['vacancy_title'],
            description=row['vacancy_description'],
        ),
        axis=1,
    )

    feature_data['has_salary_mention'] = feature_data[
        'combined_text'
    ].apply(
        lambda text: contains_keyword(
            text=text,
            keywords=SALARY_KEYWORDS,
        ),
    )
    feature_data['has_schedule_mention'] = feature_data[
        'combined_text'
    ].apply(
        lambda text: contains_keyword(
            text=text,
            keywords=SCHEDULE_KEYWORDS,
        ),
    )
    feature_data['has_requirements_mention'] = feature_data[
        'combined_text'
    ].apply(
        lambda text: contains_keyword(
            text=text,
            keywords=REQUIREMENTS_KEYWORDS,
        ),
    )
    feature_data['has_benefits_mention'] = feature_data[
        'combined_text'
    ].apply(
        lambda text: contains_keyword(
            text=text,
            keywords=BENEFITS_KEYWORDS,
        ),
    )
    feature_data['has_call_to_action'] = feature_data[
        'combined_text'
    ].apply(
        lambda text: contains_keyword(
            text=text,
            keywords=CALL_TO_ACTION_KEYWORDS,
        ),
    )

    return feature_data


def build_text_feature_rows(
    data: pd.DataFrame,
    feature_run_id: int,
) -> list[dict[str, int | bool | datetime]]:
    """Build text feature rows for persistence.
    Args:
        data (pd.DataFrame): Input snapshot dataframe.
        feature_run_id (int): Feature run identifier.
    """
    feature_data = build_text_feature_dataframe(data=data)

    if feature_data.empty:
        return []

    rows = []

    for _, row in feature_data.iterrows():
        rows.append(
            {
                'feature_run_id': feature_run_id,
                'client_id': int(row['client_id']),
                'company_id': int(row['company_id']),
                'vacancy_id': int(row['vacancy_id']),
                'date_day': row['date_day'],
                'title_length': int(row['title_length']),
                'description_length': int(row['description_length']),
                'title_word_count': int(row['title_word_count']),
                'description_word_count': int(
                    row['description_word_count'],
                ),
                'has_description': bool(row['has_description']),
                'description_is_empty': bool(row['description_is_empty']),
                'has_salary_mention': bool(row['has_salary_mention']),
                'has_schedule_mention': bool(row['has_schedule_mention']),
                'has_requirements_mention': bool(
                    row['has_requirements_mention'],
                ),
                'has_benefits_mention': bool(
                    row['has_benefits_mention'],
                ),
                'has_call_to_action': bool(row['has_call_to_action']),
            },
        )

    return rows
