from botocore.exceptions import ClientError

from api.response import ApiErrorData
from config.settings import settings
from core.infra.s3.config import get_s3_client


def delete_file_s3(s3_key: str) -> tuple[bool | None, ApiErrorData | None, bool]:
    try:
        s3_client = get_s3_client()

        try:
            s3_client.head_object(Bucket=settings.s3_bucket_name, Key=s3_key)
        except ClientError as error:
            if error.response["Error"]["Code"] == "404":
                return None, ApiErrorData(
                    message=f"Nie znaleziono pliku w S3 dla klucza: {s3_key}",
                    type_module="delete_file_s3",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False
            raise

        s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=s3_key)

        return True, None, True
    except Exception as error:
        return None, ApiErrorData(
            message=str(error),
            type_module="delete_file_s3",
            type_error="exception",
            key_type_error="Exception",
        ), False
