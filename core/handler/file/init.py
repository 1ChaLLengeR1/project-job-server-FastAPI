from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.infra.s3.init import initialization_url_upload_file
from core.infra.s3.response import S3InitUploadFileResponse
from core.repository.psql.logs.create import create_logs_psql
from database.psql.models.file import FileType


def handler_init_upload_file(
    user_id: str,
    name: str,
    original_name: str,
    size: int,
    file_type: FileType,
    mime_type: str,
    catalog: str,
    db_session: Session | None = None,
) -> tuple[S3InitUploadFileResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = initialization_url_upload_file(
            user_id=user_id,
            name=name,
            original_name=original_name,
            size=size,
            file_type=file_type,
            mime_type=mime_type,
            catalog=catalog,
            db_session=db_session,
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:init", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_init_upload_file",
            type_error="exception",
            key_type_error="Exception",
        ), False
