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
        extra="ignore",
    )

    # Baza danych
    db_host: str = Field(validation_alias="DB_HOST")
    db_port: int = Field(validation_alias="DB_PORT", ge=1, le=65535)
    db_user: str = Field(validation_alias="DB_USER")
    db_password: str = Field(validation_alias="DB_PASSWORD")
    db_name: str = Field(validation_alias="DB_DBNAME")

    # JWT
    secret_key_token: str = Field(validation_alias="SECRET_KEY_TOKEN", min_length=1)
    secret_key_refresh_token: str = Field(validation_alias="SECRET_KEY_REFRESH_TOKEN", min_length=1)
    # wspólny sekret tokena kontaktowego (X-Contact-Token) — podpisują nim klienci
    # publicznego endpointu /contact/messages/create (frontendy i backendy)
    secret_key_contact_token: str = Field(validation_alias="SECRET_KEY_CONTACT_TOKEN", min_length=1)
    algorithm: str = Field(validation_alias="ALGORITHM")
    token_expires_hours: int = Field(validation_alias="TOKEN_EXPIRES_HOURS", gt=0)
    refresh_token_expires_hours: int = Field(validation_alias="REFRESH_TOKEN_EXPIRES_HOURS", gt=0)


settings = Settings()
