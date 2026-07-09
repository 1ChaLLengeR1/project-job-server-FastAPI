from datetime import date

from sqlalchemy.exc import IntegrityError
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


def create_apartment_psql(
    name: str, description: str | None = None, is_active: bool = True, db_session: Session | None = None
) -> tuple[ApartmentResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_apartment = RentalApartment(name=name, description=description, is_active=is_active)
            db.add(new_apartment)
            db.flush()
            db.refresh(new_apartment)
            return _to_apartment_response(new_apartment), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_apartment_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="create_apartment_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def create_tenant_psql(
    first_name: str,
    last_name: str | None = None,
    note: str | None = None,
    is_active: bool = True,
    db_session: Session | None = None,
) -> tuple[TenantResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_tenant = RentalTenant(first_name=first_name, last_name=last_name, note=note, is_active=is_active)
            db.add(new_tenant)
            db.flush()
            db.refresh(new_tenant)
            return _to_tenant_response(new_tenant), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_tenant_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="create_tenant_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def create_tenancy_psql(
    apartment_id: str,
    tenant_id: str,
    rent_amount: float,
    persons_count: int,
    start_date: date,
    end_date: date | None = None,
    db_session: Session | None = None,
) -> tuple[TenancyResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_tenancy = RentalTenancy(
                apartment_id=apartment_id,
                tenant_id=tenant_id,
                rent_amount=rent_amount,
                persons_count=persons_count,
                start_date=start_date,
                end_date=end_date,
            )
            db.add(new_tenancy)
            db.flush()
            db.refresh(new_tenancy)
            return _to_tenancy_response(new_tenancy), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_tenancy_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="create_tenancy_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def create_cost_type_psql(
    name: str, charge_type: str, is_active: bool = True, db_session: Session | None = None
) -> tuple[CostTypeResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_cost_type = RentalCostType(name=name, charge_type=charge_type, is_active=is_active)
            db.add(new_cost_type)
            db.flush()
            db.refresh(new_cost_type)
            return _to_cost_type_response(new_cost_type), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_cost_type_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="create_cost_type_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def create_apartment_cost_psql(
    apartment_id: str,
    cost_type_id: str,
    amount: float,
    start_date: date,
    end_date: date | None = None,
    db_session: Session | None = None,
) -> tuple[ApartmentCostResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_apartment_cost = RentalApartmentCost(
                apartment_id=apartment_id,
                cost_type_id=cost_type_id,
                amount=amount,
                start_date=start_date,
                end_date=end_date,
            )
            db.add(new_apartment_cost)
            db.flush()
            db.refresh(new_apartment_cost)
            return _to_apartment_cost_response(new_apartment_cost), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_apartment_cost_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="create_apartment_cost_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def create_meter_psql(
    media_type: str,
    apartment_id: str | None = None,
    is_master: bool = False,
    name: str | None = None,
    is_active: bool = True,
    db_session: Session | None = None,
) -> tuple[MeterResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_meter = RentalMeter(
                apartment_id=apartment_id,
                media_type=media_type,
                is_master=is_master,
                name=name,
                is_active=is_active,
            )
            db.add(new_meter)
            db.flush()
            db.refresh(new_meter)
            return _to_meter_response(new_meter), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_meter_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="create_meter_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
