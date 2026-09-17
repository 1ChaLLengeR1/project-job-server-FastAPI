from uuid import uuid4

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from config.settings import settings
from core.infra.s3.config import get_s3_client
from core.infra.s3.response import S3InitUploadFileResponse
from core.repository.psql.file.create import create_file_psql
from database.psql.models.file import FileType


def initialization_url_upload_file(
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
        unique_name = f"{uuid4()}_{name}"
        s3_key = f"{catalog}/{unique_name}"

        # bucket jest prywatny - goly URL S3 nie dziala bez podpisu, wiec nie budujemy
        # i nie zapisujemy go w ogole (jedyny dzialajacy dostep to presigned URL:
        # `signed_url` ponizej przy uploadzie, `preview`/`download` pozniej)
        file, error, success = create_file_psql(
            user_id=user_id,
            name=unique_name,
            original_name=original_name,
            size=size,
            file_type=file_type,
            mime_type=mime_type,
            s3_key=s3_key,
            s3_prefix=catalog,
            url=None,
            db_session=db_session,
        )

        if not success:
            return None, error, False

        s3_client = get_s3_client()
        signed_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.s3_bucket_name,
                "Key": s3_key,
                "ContentType": mime_type,
            },
            ExpiresIn=900,
        )

        return S3InitUploadFileResponse(
            file_id=file.id,
            signed_url=signed_url,
            url=None,
        ), None, True
    except Exception as error:
        return None, ApiErrorData(
            message=str(error),
            type_module="initialization_url_upload_file",
            type_error="exception",
            key_type_error="Exception",
        ), False
