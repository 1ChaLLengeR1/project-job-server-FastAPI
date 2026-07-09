from datetime import date

from sqlalchemy import or_
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.rental.dictionaries.response import (
    ApartmentCostResponse,
    ApartmentResponse,
    CostTypeResponse,
    MeterResponse,
    TenancyResponse,
    TenantResponse,
    _to_apartment_cost_response,
    _to_apartment_response,
    _to_cost_type_response,
    _to_meter_response,
    _to_tenancy_response,
    _to_tenant_response,
)
from database.psql.database import managed_session
from database.psql.models.rentals import (
    RentalApartment,
    RentalApartmentCost,
    RentalCostType,
    RentalMeter,
    RentalTenancy,
    RentalTenant,
)


def collection_apartments_psql(
    is_active: bool | None = None, db_session: Session | None = None
) -> tuple[list[ApartmentResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(RentalApartment)
            if is_active is not None:
                query = query.filter(RentalApartment.is_active == is_active)
            apartments = query.order_by(RentalApartment.name.asc()).all()
            return [_to_apartment_response(apartment) for apartment in apartments], None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_apartments_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def collection_tenants_psql(
    is_active: bool | None = None, db_session: Session | None = None
) -> tuple[list[TenantResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(RentalTenant)
            if is_active is not None:
                query = query.filter(RentalTenant.is_active == is_active)
            tenants = query.order_by(RentalTenant.first_name.asc()).all()
            return [_to_tenant_response(tenant) for tenant in tenants], None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_tenants_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def collection_tenancies_psql(
    apartment_id: str | None = None,
    tenant_id: str | None = None,
    active_on: date | None = None,
    db_session: Session | None = None,
) -> tuple[list[TenancyResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(RentalTenancy)
            if apartment_id is not None:
                query = query.filter(RentalTenancy.apartment_id == apartment_id)
            if tenant_id is not None:
                query = query.filter(RentalTenancy.tenant_id == tenant_id)
            if active_on is not None:
                query = query.filter(RentalTenancy.start_date <= active_on).filter(
                    or_(RentalTenancy.end_date.is_(None), RentalTenancy.end_date >= active_on)
                )
            tenancies = query.order_by(RentalTenancy.start_date.desc()).all()
            return [_to_tenancy_response(tenancy) for tenancy in tenancies], None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_tenancies_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def collection_cost_types_psql(
    is_active: bool | None = None, db_session: Session | None = None
) -> tuple[list[CostTypeResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(RentalCostType)
            if is_active is not None:
                query = query.filter(RentalCostType.is_active == is_active)
            cost_types = query.order_by(RentalCostType.name.asc()).all()
            return [_to_cost_type_response(cost_type) for cost_type in cost_types], None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_cost_types_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def collection_apartment_costs_psql(
    apartment_id: str | None = None,
    active_on: date | None = None,
    db_session: Session | None = None,
) -> tuple[list[ApartmentCostResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(RentalApartmentCost)
            if apartment_id is not None:
                query = query.filter(RentalApartmentCost.apartment_id == apartment_id)
            if active_on is not None:
                query = query.filter(RentalApartmentCost.start_date <= active_on).filter(
                    or_(RentalApartmentCost.end_date.is_(None), RentalApartmentCost.end_date >= active_on)
                )
            apartment_costs = query.order_by(RentalApartmentCost.start_date.desc()).all()
            return [_to_apartment_cost_response(apartment_cost) for apartment_cost in apartment_costs], None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_apartment_costs_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def collection_meters_psql(
    apartment_id: str | None = None,
    media_type: str | None = None,
    is_active: bool | None = None,
    db_session: Session | None = None,
) -> tuple[list[MeterResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(RentalMeter)
            if apartment_id is not None:
                query = query.filter(RentalMeter.apartment_id == apartment_id)
            if media_type is not None:
                query = query.filter(RentalMeter.media_type == media_type)
            if is_active is not None:
                query = query.filter(RentalMeter.is_active == is_active)
            meters = query.order_by(RentalMeter.created_at.asc()).all()
            return [_to_meter_response(meter) for meter in meters], None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_meters_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
