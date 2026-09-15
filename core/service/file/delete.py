from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.infra.s3.delete import delete_file_s3
from core.repository.psql.file.delete import delete_file_psql
from core.service.file.response import ServiceDeleteFileResponse


def delete_file_service(
    file_id: str, db_session: Session | None = None
) -> tuple[ServiceDeleteFileResponse | None, ApiErrorData | None, bool]:
    try:
        deleted_file, error, success = delete_file_psql(file_id=file_id, db_session=db_session)
        if not success:
            return None, error, False

        _, s3_error, s3_success = delete_file_s3(s3_key=deleted_file.s3_key)
        if not s3_success:
            return None, ApiErrorData(
                message=s3_error.message,
                type_module="delete_file_service",
                type_error="s3_error",
                key_type_error="S3DeleteFailed",
            ), False

        return ServiceDeleteFileResponse(file_id=deleted_file.id), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="delete_file_service",
            type_error="exception",
            key_type_error="Exception",
        ), False
