from sqlalchemy.orm import Session

from api.response import ApiErrorData
from config.settings import settings
from core.infra.s3.get import generate_get_presigned_url
from core.repository.psql.file.view import get_viewable_file_psql
from core.service.file.response import ServiceFileUrlResponse


def download_file_service(
    file_id: str, db_session: Session | None = None
) -> tuple[ServiceFileUrlResponse | None, ApiErrorData | None, bool]:
    try:
        file, error, success = get_viewable_file_psql(file_id, db_session=db_session)
        if not success:
            return None, error, False

        expires_seconds = settings.file_download_url_expire_seconds
        signed_url, s3_error, s3_success = generate_get_presigned_url(
            s3_key=file.s3_key,
            expires_seconds=expires_seconds,
            disposition="attachment",
            filename=file.original_name,
        )
        if not s3_success:
            return None, s3_error, False

        return ServiceFileUrlResponse(
            file_id=file.id, url=signed_url, expires_in_seconds=expires_seconds
        ), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="download_file_service",
            type_error="exception",
            key_type_error="Exception",
        ), False
