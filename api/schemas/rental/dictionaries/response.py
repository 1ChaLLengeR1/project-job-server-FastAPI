from datetime import date, datetime

from pydantic import BaseModel


class RentalApartmentResponseData(BaseModel):
    id: str
    name: str
    description: str | None
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None


class RentalTenantResponseData(BaseModel):
    id: str
    first_name: str
    last_name: str | None
    note: str | None
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None


class RentalTenancyResponseData(BaseModel):
    id: str
    apartment_id: str
    tenant_id: str
    rent_amount: float
    persons_count: int
    start_date: date
    end_date: date | None
    created_at: datetime | None
    updated_at: datetime | None


class RentalCostTypeResponseData(BaseModel):
    id: str
    name: str
    charge_type: str
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None


class RentalApartmentCostResponseData(BaseModel):
    id: str
    apartment_id: str
    cost_type_id: str
    amount: float
    start_date: date
    end_date: date | None
    created_at: datetime | None
    updated_at: datetime | None


class RentalMeterResponseData(BaseModel):
    id: str
    apartment_id: str | None
    media_type: str
    is_master: bool
    name: str | None
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None
