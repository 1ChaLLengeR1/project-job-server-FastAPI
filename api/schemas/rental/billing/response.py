from datetime import date, datetime

from pydantic import BaseModel, Field


class RentalBillingPeriodResponseData(BaseModel):
    id: str
    period_month: date
    status: str
    electricity_bill_amount: float | None
    electricity_rate: float | None
    electricity_rate_is_manual: bool
    water_rate: float
    note: str | None
    created_at: datetime | None
    updated_at: datetime | None


class RentalMeterReadingResponseData(BaseModel):
    id: str
    period_id: str
    meter_id: str
    previous_value: float
    current_value: float
    error_correction: float
    created_at: datetime | None
    updated_at: datetime | None


class RentalSettlementItemResponseData(BaseModel):
    id: str
    settlement_id: str
    cost_type_id: str | None
    name: str
    kind: str
    amount: float
    created_at: datetime | None
    updated_at: datetime | None


class RentalSettlementResponseData(BaseModel):
    id: str
    period_id: str
    apartment_id: str
    tenancy_id: str | None
    rent_amount: float
    electricity_consumption: float
    electricity_cost: float
    water_consumption: float
    water_cost: float
    total_media_amount: float
    total_amount: float
    note: str | None
    created_at: datetime | None
    updated_at: datetime | None
    items: list[RentalSettlementItemResponseData] = Field(default_factory=list)


# --- Preview / close: pełne wyliczenie okresu (odpowiednik jednego pliku Obliczenia*.txt) ---


class RentalMeterConsumptionData(BaseModel):
    meter_id: str
    apartment_id: str | None
    media_type: str
    raw_difference: float
    consumption: float
    error_correction: float
    is_master: bool


class RentalMeterErrorProposalData(BaseModel):
    meter_id: str
    apartment_id: str | None
    proposed_correction: float


class RentalMainMeterErrorData(BaseModel):
    main_difference: float
    apartments_total: float
    error: float
    proposals: list[RentalMeterErrorProposalData] = Field(default_factory=list)


class RentalSettlementItemCalcData(BaseModel):
    name: str
    kind: str
    amount: float
    cost_type_id: str | None = None


class RentalApartmentSettlementData(BaseModel):
    apartment_id: str
    tenancy_id: str | None
    rent_amount: float
    electricity_consumption: float
    electricity_cost: float
    water_consumption: float
    water_cost: float
    total_media_amount: float
    total_amount: float
    items: list[RentalSettlementItemCalcData] = Field(default_factory=list)


class RentalPeriodSettlementPreviewData(BaseModel):
    apartment_id: str
    apartment_name: str
    settlement: RentalApartmentSettlementData


class RentalBeneficiaryAllocationItemData(BaseModel):
    description: str
    amount: float
    rule_id: str | None = None
    settlement_id: str | None = None


class RentalPeriodBeneficiaryPreviewData(BaseModel):
    beneficiary_id: str
    beneficiary_name: str
    total_amount: float
    items: list[RentalBeneficiaryAllocationItemData] = Field(default_factory=list)


class RentalPeriodPreviewResponseData(BaseModel):
    period: RentalBillingPeriodResponseData
    electricity_rate: float
    electricity_total_consumption: float
    main_meter_error: RentalMainMeterErrorData | None
    consumptions: list[RentalMeterConsumptionData] = Field(default_factory=list)
    settlements: list[RentalPeriodSettlementPreviewData] = Field(default_factory=list)
    beneficiaries: list[RentalPeriodBeneficiaryPreviewData] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
