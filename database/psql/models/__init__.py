# Kompletny rejestr modeli ORM - import tego pakietu rejestruje wszystkie
# metadane (wymagane przez alembic autogenerate i konfigurację mapperów).
from database.psql.models import (  # noqa: F401
    auth,
    calendar,
    logs,
    outstanding_money,
    patryk,
    tasks,
)
