"""Fixtures globalne — testowa baza danych (wzorzec: docs/ARCHITEKTURA.md, sekcja 12).

Realny lokalny Postgres: DROP/CREATE bazy `{db_name}_test`, schemat przez
Base.metadata.create_all. Izolacja testów przez TRUNCATE ... CASCADE po każdym
teście. Funkcje _psql dostają `db_session` z fixture — managed_session reużywa
sesji i nie commituje (commit kontroluje test/fixture).
"""

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

import database.psql.models.auth  # noqa: F401 — rejestracja metadanych
import database.psql.models.calendar  # noqa: F401
import database.psql.models.logs  # noqa: F401
import database.psql.models.outstanding_money  # noqa: F401
import database.psql.models.patryk  # noqa: F401
import database.psql.models.rentals  # noqa: F401
import database.psql.models.tasks  # noqa: F401
from config.settings import settings
from database.psql.base import Base

TEST_DB_NAME = f"{settings.db_name}_test"


def _db_url(database: str) -> URL:
    return URL.create(
        drivername="postgresql",
        username=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port,
        database=database,
    )


@pytest.fixture(scope="session", autouse=True)
def test_engine():
    admin_engine = create_engine(_db_url("postgres"), isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        conn.execute(
            text("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = :db"),
            {"db": TEST_DB_NAME},
        )
        conn.execute(text(f'DROP DATABASE IF EXISTS "{TEST_DB_NAME}"'))
        conn.execute(text(f'CREATE DATABASE "{TEST_DB_NAME}"'))
    admin_engine.dispose()

    engine = create_engine(_db_url(TEST_DB_NAME))
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = session_factory()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(autouse=True)
def clean_tables(test_engine, db_session):
    yield
    db_session.rollback()
    db_session.close()
    with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f'TRUNCATE TABLE "{table.name}" CASCADE'))
