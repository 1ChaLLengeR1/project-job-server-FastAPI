from datetime import date, timedelta

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import (
    RepositoryCollectionFilePagination,
    RepositoryCollectionFileResponse,
    _to_file_response,
)
from database.psql.database import managed_session
from database.psql.models.file import File

EXPIRING_WITHIN_DAYS = 30


def collection_expiring_guarantees_psql(
    limit: int = 32,
    offset: int = 0,
    db_session: Session | None = None,
) -> tuple[RepositoryCollectionFileResponse | None, ApiErrorData | None, bool]:
    """Skrot z planu (sekcja 5.5): gwarancje konczace sie w ciagu najblizszych
    EXPIRING_WITHIN_DAYS dni, jeszcze nie wygasle - posortowane po dacie konca
    rosnaco (najpilniejsze pierwsze)."""
    try:
        with managed_session(db_session) as (db, _):
            today = date.today()
            threshold = today + timedelta(days=EXPIRING_WITHIN_DAYS)
            query = db.query(File).filter(
                File.guarantee_end_date.isnot(None),
                File.guarantee_end_date >= today,
                File.guarantee_end_date <= threshold,
            )

            total = query.count()
            files = query.order_by(File.guarantee_end_date.asc()).limit(limit).offset(offset).all()
            page = (offset // limit) + 1 if limit > 0 else 1

            return RepositoryCollectionFileResponse(
                data=[_to_file_response(file) for file in files],
                pagination=RepositoryCollectionFilePagination(
                    has_more=(offset + limit) < total,
                    page=page,
                    limit=limit,
                    offset=offset,
                    total=total,
                ),
            ), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="collection_expiring_guarantees_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
