from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import (
    RepositoryCollectionFilePagination,
    RepositoryCollectionFileResponse,
    _to_file_response,
)
from database.psql.database import managed_session
from database.psql.models.file import File, FileType


def collection_files_psql(
    limit: int = 32,
    offset: int = 0,
    file_type: str | None = None,
    original_name: str | None = None,
    catalog: str | None = None,
    db_session: Session | None = None,
) -> tuple[RepositoryCollectionFileResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(File)

            if file_type is not None:
                query = query.filter(File.file_type == FileType(file_type))

            if original_name is not None:
                query = query.filter(File.original_name.ilike(f"%{original_name}%"))

            if catalog is not None:
                query = query.filter(File.s3_prefix == catalog)

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
            type_module="collection_files_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
