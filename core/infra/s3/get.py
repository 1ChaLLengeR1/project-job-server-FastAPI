from urllib.parse import quote

from api.response import ApiErrorData
from config.settings import settings
from core.infra.s3.config import get_s3_client


def _build_content_disposition(disposition: str, filename: str | None) -> str:
    """`ResponseContentDisposition` musi dac sie zakodowac w ISO-8859-1 (tak
    wymaga S3/HTTP) - polskie znaki (np. 'Ś') tego nie spelniaja i S3 zwraca
    `InvalidArgument`. Fallback `filename=` (ASCII, nieczytelne znaki -> '?')
    dla starych klientow + `filename*=UTF-8''...` (RFC 6266, percent-encoded,
    zawsze czysty ASCII) z pelna nazwa dla wspolczesnych przegladarek."""
    if not filename:
        return disposition
    ascii_fallback = filename.encode("ascii", "replace").decode("ascii").replace('"', "_")
    encoded_filename = quote(filename, safe="")
    return f"{disposition}; filename=\"{ascii_fallback}\"; filename*=UTF-8''{encoded_filename}"


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
        content_disposition = _build_content_disposition(disposition, filename)

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
