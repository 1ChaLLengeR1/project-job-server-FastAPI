import boto3
from botocore.client import BaseClient, Config
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, UnknownServiceError

from config.settings import settings
from core.exceptions.exceptions import ExternalServiceError


def get_s3_client() -> BaseClient:
    try:
        return boto3.client(
            service_name="s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
            config=Config(signature_version="s3v4"),
        )
    except NoCredentialsError as error:
        raise ExternalServiceError(
            "Brak poświadczeń AWS.", type_module="get_s3_client", type_error="no_credentials"
        ) from error
    except PartialCredentialsError as error:
        raise ExternalServiceError(
            "Niekompletne poświadczenia AWS.", type_module="get_s3_client", type_error="partial_credentials"
        ) from error
    except UnknownServiceError as error:
        raise ExternalServiceError(
            f"Nieznana usługa AWS: {error}", type_module="get_s3_client", type_error="unknown_service"
        ) from error
