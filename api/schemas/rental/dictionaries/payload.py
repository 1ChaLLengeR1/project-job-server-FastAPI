from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from api.validators import validate_non_empty_str, validate_uuid


class RentalApartmentCreatePayload(BaseModel):
    name: str = Field(max_length=255, description="Nazwa mieszkania, np. 'Pokój Państwa Dudzik'")
    description: str | None = Field(default=None, description="Opis mieszkania")
    is_active: bool = Field(default=True, description="Czy mieszkanie jest aktywne")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class RentalApartmentUpdatePayload(BaseModel):
    name: str = Field(max_length=255, description="Nowa nazwa mieszkania")
    description: str | None = Field(default=None, description="Nowy opis mieszkania")
    is_active: bool = Field(description="Nowy stan aktywności mieszkania")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class RentalTenantCreatePayload(BaseModel):
    first_name: str = Field(max_length=255, description="Imię najemcy")
    last_name: str | None = Field(default=None, max_length=255, description="Nazwisko najemcy")
    note: str | None = Field(default=None, description="Notatka (telefon, uwagi)")
    is_active: bool = Field(default=True, description="Czy najemca jest aktywny")

    @field_validator("first_name")
    @classmethod
    def first_name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class RentalTenantUpdatePayload(BaseModel):
    first_name: str = Field(max_length=255, description="Nowe imię najemcy")
    last_name: str | None = Field(default=None, max_length=255, description="Nowe nazwisko najemcy")
    note: str | None = Field(default=None, description="Nowa notatka (telefon, uwagi)")
    is_active: bool = Field(description="Nowy stan aktywności najemcy")

    @field_validator("first_name")
    @classmethod
    def first_name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class RentalTenancyCreatePayload(BaseModel):
    apartment_id: str = Field(description="UUID mieszkania")
    tenant_id: str = Field(description="UUID najemcy")
    rent_amount: float = Field(ge=0, description="Czynsz deklarowany dla tego najmu")
    persons_count: int = Field(default=1, gt=0, description="Liczba osób (do kosztów per osoba)")
    start_date: date = Field(description="Początek najmu")
    end_date: date | None = Field(default=None, description="Koniec najmu (NULL = najem trwa)")

    @field_validator("apartment_id", "tenant_id")
    @classmethod
    def ids_valid_uuid(cls, value: str) -> str:
        return validate_uuid(value)


class RentalTenancyUpdatePayload(BaseModel):
    rent_amount: float = Field(ge=0, description="Nowy czynsz deklarowany")
    persons_count: int = Field(gt=0, description="Nowa liczba osób")
    start_date: date = Field(description="Nowy początek najmu")
    end_date: date | None = Field(default=None, description="Nowy koniec najmu (NULL = najem trwa)")


class RentalCostTypeCreatePayload(BaseModel):
    name: str = Field(max_length=255, description="Nazwa rodzaju kosztu, np. 'śmieci', 'internet'")
    charge_type: Literal["fixed", "per_person"] = Field(description="Sposób naliczania: fixed | per_person")
    is_active: bool = Field(default=True, description="Czy rodzaj kosztu jest aktywny")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class RentalCostTypeUpdatePayload(BaseModel):
    name: str = Field(max_length=255, description="Nowa nazwa rodzaju kosztu")
    charge_type: Literal["fixed", "per_person"] = Field(description="Nowy sposób naliczania: fixed | per_person")
    is_active: bool = Field(description="Nowy stan aktywności rodzaju kosztu")

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class RentalApartmentCostCreatePayload(BaseModel):
    apartment_id: str = Field(description="UUID mieszkania")
    cost_type_id: str = Field(description="UUID rodzaju kosztu")
    amount: float = Field(ge=0, description="Kwota (dla per_person - stawka za osobę)")
    start_date: date = Field(description="Początek obowiązywania stawki")
    end_date: date | None = Field(default=None, description="Koniec obowiązywania (NULL = obowiązuje)")

    @field_validator("apartment_id", "cost_type_id")
    @classmethod
    def ids_valid_uuid(cls, value: str) -> str:
        return validate_uuid(value)


class RentalApartmentCostUpdatePayload(BaseModel):
    amount: float = Field(ge=0, description="Nowa kwota (dla per_person - stawka za osobę)")
    start_date: date = Field(description="Nowy początek obowiązywania stawki")
    end_date: date | None = Field(default=None, description="Nowy koniec obowiązywania (NULL = obowiązuje)")


class RentalMeterCreatePayload(BaseModel):
    media_type: Literal["electricity", "water"] = Field(description="Rodzaj medium: electricity | water")
    apartment_id: str | None = Field(default=None, description="UUID mieszkania (NULL = licznik główny budynku)")
    is_master: bool = Field(default=False, description="Licznik nadrzędny (zużycie = odczyt - suma pozostałych)")
    name: str | None = Field(default=None, max_length=255, description="Nazwa licznika")
    is_active: bool = Field(default=True, description="Czy licznik jest aktywny")

    @field_validator("apartment_id")
    @classmethod
    def apartment_id_valid_uuid(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_uuid(value)


class RentalMeterUpdatePayload(BaseModel):
    is_master: bool = Field(description="Nowy stan flagi licznika nadrzędnego")
    name: str | None = Field(default=None, max_length=255, description="Nowa nazwa licznika")
    is_active: bool = Field(description="Nowy stan aktywności licznika")
