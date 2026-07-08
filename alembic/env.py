from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import URL

# import pakietu modeli rejestruje wszystkie metadane (autogenerate)
import database.psql.models  # noqa: F401
from alembic import context

# get_env_variable ładuje env/{ENV_MODE}.env i czyta zmienne środowiskowe
# (env procesu ma priorytet - CI działa bez plików env/)
from core.helper.validators import get_env_variable
from database.psql.base import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

database_url = URL.create(
    drivername="postgresql",
    username=get_env_variable("DB_USER"),
    password=get_env_variable("DB_PASSWORD"),
    host=get_env_variable("DB_HOST"),
    port=int(get_env_variable("DB_PORT")),
    database=get_env_variable("DB_DBNAME"),
)


def run_migrations_offline() -> None:
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = database_url.render_as_string(hide_password=False)

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
