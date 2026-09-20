from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.service.file.delete import delete_file_service
from core.service.file.response import ServiceDeleteFileResponse


def handler_delete_file(
    user_id: str, file_id: str, db_session: Session | None = None
) -> tuple[ServiceDeleteFileResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = delete_file_service(file_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:delete_file", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_delete_file",
            type_error="exception",
            key_type_error="Exception",
        ), False
