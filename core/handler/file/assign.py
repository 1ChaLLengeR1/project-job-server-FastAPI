from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.assign import assign_file_psql
from core.repository.psql.file.response import FileResponse
from core.repository.psql.logs.create import create_logs_psql


def handler_assign_file(
    user_id: str,
    file_id: str,
    node_id: str,
    parent_file_id: str | None = None,
    db_session: Session | None = None,
) -> tuple[FileResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = assign_file_psql(file_id, node_id, parent_file_id=parent_file_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:assign", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_assign_file",
            type_error="exception",
            key_type_error="Exception",
        ), False
