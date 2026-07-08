from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.helper.validators import get_env_variable

host = get_env_variable("DB_HOST")
port = get_env_variable("DB_PORT")
user = get_env_variable("DB_USER")
password = get_env_variable("DB_PASSWORD")
db_name = get_env_variable("DB_DBNAME")

data_base_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
engine = create_engine(data_base_url, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def managed_session(db_session: Session | None = None):
    """Context manager warstwy repository (wzorzec z docs/ARCHITEKTURA.md 9.1).

    Jeśli sesja przyszła z zewnątrz (endpoint / Depends(get_db)) - reużywa jej,
    commit należy do właściciela. Jeśli None - tworzy własną i sama commituje.
    """
    if db_session is not None:
        yield db_session, False
        return

    db = SessionLocal()
    try:
        yield db, True
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
