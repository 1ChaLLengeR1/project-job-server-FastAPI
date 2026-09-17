from api.response import ApiErrorData
from config.settings import settings
from core.infra.s3.config import get_s3_client


def generate_get_presigned_url(
    s3_key: str,
    expires_seconds: int,
    disposition: str,
    filename: str | None = None,
) -> tuple[str | None, ApiErrorData | None, bool]:
    """Wspolna funkcja dla podgladu (`disposition="inline"`) i pobierania
    (`disposition="attachment"`, wymusza pobranie pod `filename`) - zob.
    PLAN_MAGAZYN_PLIKOW.md sekcja 4, punkt 3."""
    try:
        s3_client = get_s3_client()
        content_disposition = f'{disposition}; filename="{filename}"' if filename else disposition

        signed_url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": settings.s3_bucket_name,
                "Key": s3_key,
                "ResponseContentDisposition": content_disposition,
            },
            ExpiresIn=expires_seconds,
        )
        return signed_url, None, True
    except Exception as error:
        return None, ApiErrorData(
            message=str(error),
            type_module="generate_get_presigned_url",
            type_error="exception",
            key_type_error="Exception",
        ), False
