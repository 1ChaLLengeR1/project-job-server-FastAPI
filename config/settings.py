from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.app_config import ENV_PATH


class Settings(BaseSettings):
    """Konfiguracja aplikacji (wzorzec: docs/ARCHITEKTURA.md 7.1).

    Czyta env/{ENV_MODE}.env, przy czym zmienne środowiskowe procesu mają
    priorytet nad plikiem - dzięki temu CI i kontenery (docker secret)
    działają bez plików env/.
    """

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        env_prefix="BACKEND_SERVER_JOB_",
        extra="ignore",
    )

    # Baza danych
    db_host: str
    db_port: int = Field(ge=1, le=65535)
    db_user: str
    db_password: str
    # jedyny wyjątek od konwencji nazw — zmienna w env to DB_DBNAME, nie DB_NAME;
    # z alias-em `env_prefix` nie jest dokładany automatycznie, więc podajemy go w pełni
    db_name: str = Field(validation_alias="BACKEND_SERVER_JOB_DB_DBNAME")

    # JWT
    secret_key_token: str = Field(min_length=1)
    secret_key_refresh_token: str = Field(min_length=1)
    # wspólny sekret tokena kontaktowego (X-Contact-Token) — podpisują nim klienci
    # publicznego endpointu /contact/messages/create (frontendy i backendy)
    secret_key_contact_token: str = Field(min_length=1)
    algorithm: str
    token_expires_hours: int = Field(gt=0)
    refresh_token_expires_hours: int = Field(gt=0)

    # AWS / S3
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str
    s3_bucket_name: str
    s3_kms_key_id: str
    # domyślne wartości z PLAN_MAGAZYN_PLIKOW.md sekcja 4.1 - krótkoterminowe presigned GET
    file_preview_url_expire_seconds: int = Field(default=180, gt=0)
    file_download_url_expire_seconds: int = Field(default=60, gt=0)


settings = Settings()
