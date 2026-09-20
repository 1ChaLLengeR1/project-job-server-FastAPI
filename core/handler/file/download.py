from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.service.file.download import download_file_service
from core.service.file.response import ServiceFileUrlResponse


def handler_download_file(
    user_id: str, file_id: str, db_session: Session | None = None
) -> tuple[ServiceFileUrlResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = download_file_service(file_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:download", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_download_file",
            type_error="exception",
            key_type_error="Exception",
        ), False
