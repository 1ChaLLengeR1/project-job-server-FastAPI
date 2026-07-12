from typing import Literal

from pydantic import BaseModel, Field, field_validator

from api.validators import validate_uuid


class KeysCalculatorUpdatePayload(BaseModel):
    id: str = Field(description="Id rekordu kluczy kalkulatora (UUID)")
    income_tax: float = Field(ge=0, description="Podatek dochodowy (ułamek, np. 0.12)")
    vat: float = Field(ge=0, description="VAT (ułamek, np. 0.23)")
    inpost_parcel_locker: float = Field(ge=0, description="Koszt wysyłki: paczkomat InPost")
    inpost_courier: float = Field(ge=0, description="Koszt wysyłki: kurier InPost")
    inpost_cash_of_delivery_courier: float = Field(ge=0, description="Koszt wysyłki: kurier InPost za pobraniem")
    dpd: float = Field(ge=0, description="Koszt wysyłki: DPD")
    allegro_matt: float = Field(ge=0, description="Koszt wysyłki: Allegro Matt")
    without_smart: float = Field(ge=0, description="Koszt wysyłki: bez Allegro Smart")

    @field_validator("id")
    @classmethod
    def id_is_uuid(cls, value: str) -> str:
        return validate_uuid(value)


class CalculationPayload(BaseModel):
    gross_sales: float = Field(gt=0, description="Cena sprzedaży brutto")
    gross_purchase: float = Field(gt=0, description="Cena zakupu brutto")
    provision: float = Field(ge=0, description="Prowizja w procentach")
    distinction: float = Field(ge=0, description="Wyróżnienie w procentach")
    referrer: Literal[
        "inpost_parcel_locker",
        "inpost_courier",
        "inpost_cash_of_delivery_courier",
        "dpd",
        "allegro_matt",
        "without_smart",
    ] = Field(description="Sposób wysyłki (klucz cennika)")
