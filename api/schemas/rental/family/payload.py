from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from api.validators import validate_non_empty_str, validate_uuid


class RentalBeneficiaryCreatePayload(BaseModel):
    name: str = Field(max_length=255, description="Nazwa beneficjenta, np. 'Ja', 'Ojciec', 'Mama'")
    is_active: bool = Field(default=True, description="Czy beneficjent jest aktywny")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class RentalBeneficiaryUpdatePayload(BaseModel):
    name: str = Field(max_length=255, description="Nowa nazwa beneficjenta")
    is_active: bool = Field(description="Nowy stan aktywności beneficjenta")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class RentalAllocationRuleCreatePayload(BaseModel):
    beneficiary_id: str = Field(description="UUID beneficjenta")
    component: Literal["rent", "electricity", "water", "cost_type", "recurring"] = Field(
        description="Składnik podziału"
    )
    mode: Literal["fixed_amount", "full"] = Field(description="Tryb: fixed_amount | full (cała kwota składnika)")
    start_date: date = Field(description="Początek obowiązywania reguły")
    apartment_id: str | None = Field(default=None, description="UUID mieszkania (NULL = wszystkie mieszkania)")
    cost_type_id: str | None = Field(default=None, description="UUID rodzaju kosztu (wymagane dla cost_type)")
    amount: float | None = Field(
        default=None, description="Kwota (wymagana dla fixed_amount i recurring; może być ujemna)"
    )
    description: str | None = Field(default=None, max_length=255, description="Etykieta pozycji, np. 'podatek'")
    end_date: date | None = Field(default=None, description="Koniec obowiązywania (NULL = obowiązuje)")

    @field_validator("beneficiary_id")
    @classmethod
    def beneficiary_id_valid_uuid(cls, value: str) -> str:
        return validate_uuid(value)

    @field_validator("apartment_id", "cost_type_id")
    @classmethod
    def optional_ids_valid_uuid(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_uuid(value)


class RentalAllocationRuleUpdatePayload(BaseModel):
    apartment_id: str | None = Field(default=None, description="Nowy UUID mieszkania (NULL = wszystkie mieszkania)")
    component: Literal["rent", "electricity", "water", "cost_type", "recurring"] = Field(
        description="Nowy składnik podziału"
    )
    cost_type_id: str | None = Field(default=None, description="Nowy UUID rodzaju kosztu (wymagane dla cost_type)")
    mode: Literal["fixed_amount", "full"] = Field(description="Nowy tryb: fixed_amount | full")
    amount: float | None = Field(default=None, description="Nowa kwota (może być ujemna)")
    description: str | None = Field(default=None, max_length=255, description="Nowa etykieta pozycji")
    start_date: date = Field(description="Nowy początek obowiązywania reguły")
    end_date: date | None = Field(default=None, description="Nowy koniec obowiązywania (NULL = obowiązuje)")

    @field_validator("apartment_id", "cost_type_id")
    @classmethod
    def optional_ids_valid_uuid(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_uuid(value)
