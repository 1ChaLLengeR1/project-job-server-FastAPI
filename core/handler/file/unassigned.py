from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.assign import unassign_file_psql
from core.repository.psql.file.response import FileResponse, RepositoryCollectionFileResponse
from core.repository.psql.file.unassigned import collection_unassigned_files_psql
from core.repository.psql.logs.create import create_logs_psql


def handler_collection_unassigned_files(
    user_id: str,
    limit: int = 32,
    offset: int = 0,
    db_session: Session | None = None,
) -> tuple[RepositoryCollectionFileResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_unassigned_files_psql(limit=limit, offset=offset, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:unassigned", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_collection_unassigned_files",
            type_error="exception",
            key_type_error="Exception",
        ), False


def handler_unassign_file(
    user_id: str,
    file_id: str,
    db_session: Session | None = None,
) -> tuple[FileResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = unassign_file_psql(file_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:unassign", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_unassign_file",
            type_error="exception",
            key_type_error="Exception",
        ), False
