from dataclasses import dataclass
from datetime import date, datetime

from database.psql.models.rentals import (
    RentalApartment,
    RentalApartmentCost,
    RentalCostType,
    RentalMeter,
    RentalTenancy,
    RentalTenant,
)


@dataclass
class ApartmentResponse:
    id: str
    name: str
    description: str | None
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class TenantResponse:
    id: str
    first_name: str
    last_name: str | None
    note: str | None
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class TenancyResponse:
    id: str
    apartment_id: str
    tenant_id: str
    rent_amount: float
    persons_count: int
    start_date: date
    end_date: date | None
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class CostTypeResponse:
    id: str
    name: str
    charge_type: str
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class ApartmentCostResponse:
    id: str
    apartment_id: str
    cost_type_id: str
    amount: float
    start_date: date
    end_date: date | None
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class MeterResponse:
    id: str
    apartment_id: str | None
    media_type: str
    is_master: bool
    name: str | None
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None


def _to_apartment_response(model: RentalApartment) -> ApartmentResponse:
    return ApartmentResponse(
        id=str(model.id),
        name=model.name,
        description=model.description,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_tenant_response(model: RentalTenant) -> TenantResponse:
    return TenantResponse(
        id=str(model.id),
        first_name=model.first_name,
        last_name=model.last_name,
        note=model.note,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_tenancy_response(model: RentalTenancy) -> TenancyResponse:
    return TenancyResponse(
        id=str(model.id),
        apartment_id=str(model.apartment_id),
        tenant_id=str(model.tenant_id),
        rent_amount=float(model.rent_amount),
        persons_count=model.persons_count,
        start_date=model.start_date,
        end_date=model.end_date,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_cost_type_response(model: RentalCostType) -> CostTypeResponse:
    return CostTypeResponse(
        id=str(model.id),
        name=model.name,
        charge_type=model.charge_type,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_apartment_cost_response(model: RentalApartmentCost) -> ApartmentCostResponse:
    return ApartmentCostResponse(
        id=str(model.id),
        apartment_id=str(model.apartment_id),
        cost_type_id=str(model.cost_type_id),
        amount=float(model.amount),
        start_date=model.start_date,
        end_date=model.end_date,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_meter_response(model: RentalMeter) -> MeterResponse:
    return MeterResponse(
        id=str(model.id),
        apartment_id=str(model.apartment_id) if model.apartment_id else None,
        media_type=model.media_type,
        is_master=model.is_master,
        name=model.name,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
