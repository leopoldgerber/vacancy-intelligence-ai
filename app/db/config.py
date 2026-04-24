from dataclasses import dataclass
from os import getenv


@dataclass(slots=True)
class DatabaseConfig:
    """Store database settings.
    Args:
        async_url (str): Async database connection URL.
        sync_url (str): Sync database connection URL."""
    async_url: str
    sync_url: str


def get_async_database_url() -> str:
    """Build async database connection URL from environment variables.
    Args:
        """
    postgres_user = getenv('POSTGRES_USER', 'postgres')
    postgres_password = getenv('POSTGRES_PASSWORD', 'postgres')
    postgres_host = getenv('POSTGRES_HOST', 'localhost')
    postgres_port = getenv('POSTGRES_PORT', '5432')
    postgres_db = getenv('POSTGRES_DB', 'postgres')

    database_url = (
        f'postgresql+asyncpg://{postgres_user}:{postgres_password}'
        f'@{postgres_host}:{postgres_port}/{postgres_db}'
    )
    return database_url


def get_sync_database_url() -> str:
    """Build sync database connection URL from environment variables.
    Args:
        """
    postgres_user = getenv('POSTGRES_USER', 'postgres')
    postgres_password = getenv('POSTGRES_PASSWORD', 'postgres')
    postgres_host = getenv('POSTGRES_HOST', 'localhost')
    postgres_port = getenv('POSTGRES_PORT', '5432')
    postgres_db = getenv('POSTGRES_DB', 'postgres')

    database_url = (
        f'postgresql+psycopg://{postgres_user}:{postgres_password}'
        f'@{postgres_host}:{postgres_port}/{postgres_db}'
    )
    return database_url


def get_database_config() -> DatabaseConfig:
    """Create database config object.
    Args:
        """
    database_config = DatabaseConfig(
        async_url=get_async_database_url(),
        sync_url=get_sync_database_url(),
    )
    return database_config
