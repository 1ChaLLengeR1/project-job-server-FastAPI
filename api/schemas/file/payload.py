from pydantic import BaseModel, Field, field_validator

from api.validators import validate_non_empty_str
from database.psql.models.file import FileStatus, FileType


class FileInitPayload(BaseModel):
    name: str = Field(max_length=255, description="Nazwa bazowa pliku (używana do budowy klucza S3)")
    original_name: str = Field(max_length=255, description="Nazwa wyświetlana użytkownikowi")
    size: int = Field(gt=0, description="Rozmiar pliku w bajtach")
    mime_type: str = Field(max_length=255, description="MIME type pliku")
    file_type: FileType = Field(description="Typ pliku")
    catalog: str = Field(max_length=512, description="Prefiks/katalog w buckecie S3")

    @field_validator("name", "original_name", "mime_type", "catalog")
    @classmethod
    def not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class FileUpdatePayload(BaseModel):
    status: FileStatus | None = Field(
        default=None,
        description="Nowy status pliku. Wartość 'confirmed' potwierdza zakończenie uploadu.",
    )
    name: str | None = Field(default=None, max_length=255, description="Nowa nazwa pliku")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_non_empty_str(value)
