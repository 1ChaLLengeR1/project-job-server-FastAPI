import re
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

from api.validators import validate_non_empty_str

# luźny format telefonu: opcjonalny +, 6-15 cyfr, dopuszczalne spacje i myślniki
PHONE_DIGITS_PATTERN = re.compile(r"^\+?\d{6,15}$")


class ContactMessageCreatePayload(BaseModel):
    first_name: str = Field(max_length=255, description="Imię nadawcy")
    last_name: str | None = Field(default=None, max_length=255, description="Nazwisko nadawcy")
    phone_number: str = Field(max_length=30, description="Numer telefonu (opcjonalny +, 6-15 cyfr)")
    email: EmailStr | None = Field(default=None, description="Adres e-mail do odpowiedzi")
    description: str = Field(max_length=5000, description="Treść zapytania / opis zadania")

    @field_validator("first_name", "description")
    @classmethod
    def fields_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)

    @field_validator("phone_number")
    @classmethod
    def phone_number_valid(cls, value: str) -> str:
        normalized = value.strip()
        digits_only = re.sub(r"[ \-]", "", normalized)
        if not PHONE_DIGITS_PATTERN.fullmatch(digits_only):
            raise ValueError(f"'{value}' nie jest poprawnym numerem telefonu")
        return normalized


class ContactMessageUpdateStatusPayload(BaseModel):
    status: Literal["new", "read", "closed"] = Field(description="Nowy status obsługi wiadomości")
