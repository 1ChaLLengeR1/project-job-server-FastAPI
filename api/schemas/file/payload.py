from datetime import date

from pydantic import BaseModel, Field, field_validator

from api.validators import validate_non_empty_str, validate_uuid
from database.psql.models.file import FileStatus, FileType

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024


class FileInitPayload(BaseModel):
    name: str = Field(max_length=255, description="Nazwa bazowa pliku (używana do budowy klucza S3)")
    original_name: str = Field(max_length=255, description="Nazwa wyświetlana użytkownikowi")
    size: int = Field(gt=0, le=MAX_FILE_SIZE_BYTES, description="Rozmiar pliku w bajtach (max 50 MB)")
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


class FileAssignPayload(BaseModel):
    node_id: str = Field(description="UUID węzła, do którego przypisujemy plik")
    parent_file_id: str | None = Field(default=None, description="UUID pliku-rodzica (opcjonalnie)")

    @field_validator("node_id")
    @classmethod
    def node_id_valid_uuid(cls, value: str) -> str:
        return validate_uuid(value)

    @field_validator("parent_file_id")
    @classmethod
    def parent_file_id_valid_uuid(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_uuid(value)


class FileMetadataPayload(BaseModel):
    original_name: str | None = Field(default=None, max_length=255, description="Nowa nazwa wyświetlana pliku")
    node_id: str | None = Field(default=None, description="Nowy węzeł (UUID) - przeniesienie pliku")
    parent_file_id: str | None = Field(
        default=None,
        description="Nowy plik-rodzic (UUID). Jawne `null` odczepia plik-dziecko; "
        "pominięcie pola nie zmienia rodzica.",
    )
    description: str | None = Field(
        default=None, description="Nowy opis pliku. Jawne `null` czyści opis; pominięcie pola go nie rusza."
    )
    guarantee_start_date: date | None = Field(
        default=None, description="Nowa data początku gwarancji. Jawne `null` czyści; pominięcie pola nie rusza."
    )
    guarantee_end_date: date | None = Field(
        default=None, description="Nowa data końca gwarancji. Jawne `null` czyści; pominięcie pola nie rusza."
    )

    @field_validator("original_name")
    @classmethod
    def original_name_not_empty(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_non_empty_str(value)

    @field_validator("node_id", "parent_file_id")
    @classmethod
    def ids_valid_uuid(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_uuid(value)
