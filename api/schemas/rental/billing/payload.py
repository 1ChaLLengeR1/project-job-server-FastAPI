from datetime import date

from pydantic import BaseModel, Field, field_validator

from api.validators import validate_non_empty_str, validate_uuid


class RentalBillingPeriodCreatePayload(BaseModel):
    period_month: date = Field(description="Miesiąc okresu (zawsze 1. dzień miesiąca)")
    electricity_bill_amount: float | None = Field(
        default=None, ge=0, description="Kwota rachunku globalnego prądu ('Do zapłaty')"
    )
    electricity_rate: float | None = Field(default=None, ge=0, description="Stawka prądu zł/kWh")
    electricity_rate_is_manual: bool = Field(default=False, description="True = stawka prądu nadpisana ręcznie")
    water_rate: float = Field(default=9.00, ge=0, description="Stawka wody zł/m³")
    note: str | None = Field(default=None, description="Notatka do okresu")


class RentalBillingPeriodUpdatePayload(BaseModel):
    electricity_bill_amount: float | None = Field(
        default=None, ge=0, description="Nowa kwota rachunku globalnego prądu"
    )
    electricity_rate: float | None = Field(default=None, ge=0, description="Nowa stawka prądu zł/kWh")
    electricity_rate_is_manual: bool = Field(description="True = stawka prądu nadpisana ręcznie")
    water_rate: float = Field(ge=0, description="Nowa stawka wody zł/m³")
    note: str | None = Field(default=None, description="Nowa notatka do okresu")


class RentalMeterReadingCreatePayload(BaseModel):
    period_id: str = Field(description="UUID okresu rozliczeniowego")
    meter_id: str = Field(description="UUID licznika")
    previous_value: float = Field(ge=0, description="Odczyt 'Ostatnio'")
    current_value: float = Field(ge=0, description="Odczyt 'Teraz'")
    error_correction: float = Field(default=0, description="Korekta błędu licznika (może być ujemna)")

    @field_validator("period_id", "meter_id")
    @classmethod
    def ids_valid_uuid(cls, value: str) -> str:
        return validate_uuid(value)


class RentalMeterReadingUpdatePayload(BaseModel):
    previous_value: float = Field(ge=0, description="Nowy odczyt 'Ostatnio'")
    current_value: float = Field(ge=0, description="Nowy odczyt 'Teraz'")
    error_correction: float = Field(description="Nowa korekta błędu licznika (może być ujemna)")


class RentalPeriodAdjustmentPayload(BaseModel):
    apartment_id: str = Field(description="UUID mieszkania, którego dotyczy korekta")
    name: str = Field(max_length=255, description="Nazwa korekty, np. 'zaległe media', 'nadpłata'")
    amount: float = Field(description="Kwota korekty (może być ujemna)")

    @field_validator("apartment_id")
    @classmethod
    def apartment_id_valid_uuid(cls, value: str) -> str:
        return validate_uuid(value)

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value: str) -> str:
        return validate_non_empty_str(value)


class RentalPeriodComputePayload(BaseModel):
    """Wspólny payload dla preview i close - korekty jednorazowe per mieszkanie."""

    adjustments: list[RentalPeriodAdjustmentPayload] = Field(
        default_factory=list, description="Korekty jednorazowe per mieszkanie"
    )
