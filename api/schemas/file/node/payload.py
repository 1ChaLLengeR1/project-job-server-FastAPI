from pydantic import BaseModel, Field, field_validator

from api.validators import validate_non_empty_str, validate_uuid


class FilesNodeCreatePayload(BaseModel):
    name: str = Field(max_length=255, description="Nazwa węzła, np. 'Ja', 'Mama', 'Praca 2025-2026'")
    parent_id: str | None = Field(
        default=None, description="UUID węzła nadrzędnego (brak = węzeł najwyższego poziomu)"
    )
    description: str | None = Field(default=None, description="Opis węzła")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)

    @field_validator("parent_id")
    @classmethod
    def parent_id_valid_uuid(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_uuid(value)


class FilesNodeUpdatePayload(BaseModel):
    name: str | None = Field(default=None, max_length=255, description="Nowa nazwa węzła")
    description: str | None = Field(default=None, description="Nowy opis węzła")
    parent_id: str | None = Field(
        default=None,
        description="Nowy węzeł nadrzędny (UUID). Jawne `parent_id: null` przenosi węzeł na "
        "najwyższy poziom; pominięcie pola w ogóle nie zmienia rodzica.",
    )
    is_active: bool | None = Field(default=None, description="Nowy stan aktywności węzła")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_non_empty_str(value)

    @field_validator("parent_id")
    @classmethod
    def parent_id_valid_uuid(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_uuid(value)
