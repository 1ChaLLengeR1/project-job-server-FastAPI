from datetime import date, datetime

from pydantic import BaseModel, Field


class RentalBeneficiaryResponseData(BaseModel):
    id: str
    name: str
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None


class RentalAllocationRuleResponseData(BaseModel):
    id: str
    beneficiary_id: str
    apartment_id: str | None
    component: str
    cost_type_id: str | None
    mode: str
    amount: float | None
    description: str | None
    start_date: date
    end_date: date | None
    created_at: datetime | None
    updated_at: datetime | None


class RentalBeneficiarySettlementItemResponseData(BaseModel):
    id: str
    beneficiary_settlement_id: str
    description: str
    amount: float
    rule_id: str | None
    settlement_id: str | None
    created_at: datetime | None
    updated_at: datetime | None


class RentalBeneficiarySettlementResponseData(BaseModel):
    id: str
    period_id: str
    beneficiary_id: str
    total_amount: float
    created_at: datetime | None
    updated_at: datetime | None
    items: list[RentalBeneficiarySettlementItemResponseData] = Field(default_factory=list)
