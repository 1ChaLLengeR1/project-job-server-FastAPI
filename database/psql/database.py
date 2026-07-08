from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

from config.settings import settings

DATABASE_URL = URL.create(
    drivername="postgresql",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_engine(
    DATABASE_URL,
    pool_size=3,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def managed_session(
    db_session: Session | None = None,
) -> Generator[tuple[Session, bool]]:
    if db_session is not None:
        yield db_session, True
    else:
        db = SessionLocal()
        try:
            yield db, False
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
