from datetime import date

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.collection import collection_files_psql
from core.repository.psql.file.response import RepositoryCollectionFileResponse
from core.repository.psql.logs.create import create_logs_psql
from database.psql.models.file import FileStatus, FileType


def handler_collection_file(
    user_id: str,
    limit: int = 32,
    offset: int = 0,
    file_type: FileType | None = None,
    status: FileStatus | None = None,
    original_name: str | None = None,
    catalog: str | None = None,
    node_id: str | None = None,
    recursive: bool = False,
    created_at_from: date | None = None,
    created_at_to: date | None = None,
    guarantee_status: str | None = None,
    db_session: Session | None = None,
) -> tuple[RepositoryCollectionFileResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_files_psql(
            limit=limit,
            offset=offset,
            file_type=file_type,
            status=status,
            original_name=original_name,
            catalog=catalog,
            node_id=node_id,
            recursive=recursive,
            created_at_from=created_at_from,
            created_at_to=created_at_to,
            guarantee_status=guarantee_status,
            db_session=db_session,
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:collection", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_collection_file",
            type_error="exception",
            key_type_error="Exception",
        ), False
