from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.one import one_file_psql
from core.repository.psql.file.response import FileWithChildrenResponse
from core.repository.psql.logs.create import create_logs_psql


def handler_one_file(
    user_id: str, file_id: str, db_session: Session | None = None
) -> tuple[FileWithChildrenResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = one_file_psql(file_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:one", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_one_file",
            type_error="exception",
            key_type_error="Exception",
        ), False
