from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import (
    RepositoryCollectionFilePagination,
    RepositoryCollectionFileResponse,
    _to_file_response,
)
from database.psql.database import managed_session
from database.psql.models.file import File, FileStatus


def collection_unassigned_files_psql(
    limit: int = 32,
    offset: int = 0,
    db_session: Session | None = None,
) -> tuple[RepositoryCollectionFileResponse | None, ApiErrorData | None, bool]:
    """Skrot z planu (sekcja 5.4): pliki z dokonczonym uploadem, ale jeszcze
    nieprzypisane do zadnego wezla - `status=COMPLETED AND node_id IS NULL`."""
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(File).filter(File.status == FileStatus.COMPLETED, File.node_id.is_(None))

            total = query.count()
            files = query.order_by(File.created_at.desc()).limit(limit).offset(offset).all()
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
            type_module="collection_unassigned_files_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
