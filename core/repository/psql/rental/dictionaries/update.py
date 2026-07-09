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


def update_apartment_psql(
    apartment_id: str,
    new_name: str,
    new_description: str | None,
    new_is_active: bool,
    db_session: Session | None = None,
) -> tuple[ApartmentResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            apartment = db.query(RentalApartment).filter(RentalApartment.id == apartment_id).first()
            if not apartment:
                return (
                    None,
                    ApiErrorData(
                        message="Mieszkanie nie istnieje",
                        type_module="update_apartment_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            apartment.name = new_name
            apartment.description = new_description
            apartment.is_active = new_is_active
            db.flush()
            db.refresh(apartment)
            return _to_apartment_response(apartment), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="update_apartment_psql",
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
                type_module="update_apartment_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def update_tenant_psql(
    tenant_id: str,
    new_first_name: str,
    new_last_name: str | None,
    new_note: str | None,
    new_is_active: bool,
    db_session: Session | None = None,
) -> tuple[TenantResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            tenant = db.query(RentalTenant).filter(RentalTenant.id == tenant_id).first()
            if not tenant:
                return (
                    None,
                    ApiErrorData(
                        message="Najemca nie istnieje",
                        type_module="update_tenant_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            tenant.first_name = new_first_name
            tenant.last_name = new_last_name
            tenant.note = new_note
            tenant.is_active = new_is_active
            db.flush()
            db.refresh(tenant)
            return _to_tenant_response(tenant), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="update_tenant_psql",
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
                type_module="update_tenant_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def update_tenancy_psql(
    tenancy_id: str,
    new_rent_amount: float,
    new_persons_count: int,
    new_start_date: date,
    new_end_date: date | None,
    db_session: Session | None = None,
) -> tuple[TenancyResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            tenancy = db.query(RentalTenancy).filter(RentalTenancy.id == tenancy_id).first()
            if not tenancy:
                return (
                    None,
                    ApiErrorData(
                        message="Najem nie istnieje",
                        type_module="update_tenancy_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            tenancy.rent_amount = new_rent_amount
            tenancy.persons_count = new_persons_count
            tenancy.start_date = new_start_date
            tenancy.end_date = new_end_date
            db.flush()
            db.refresh(tenancy)
            return _to_tenancy_response(tenancy), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="update_tenancy_psql",
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
                type_module="update_tenancy_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def update_cost_type_psql(
    cost_type_id: str,
    new_name: str,
    new_charge_type: str,
    new_is_active: bool,
    db_session: Session | None = None,
) -> tuple[CostTypeResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            cost_type = db.query(RentalCostType).filter(RentalCostType.id == cost_type_id).first()
            if not cost_type:
                return (
                    None,
                    ApiErrorData(
                        message="Rodzaj kosztu nie istnieje",
                        type_module="update_cost_type_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            cost_type.name = new_name
            cost_type.charge_type = new_charge_type
            cost_type.is_active = new_is_active
            db.flush()
            db.refresh(cost_type)
            return _to_cost_type_response(cost_type), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="update_cost_type_psql",
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
                type_module="update_cost_type_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def update_apartment_cost_psql(
    apartment_cost_id: str,
    new_amount: float,
    new_start_date: date,
    new_end_date: date | None,
    db_session: Session | None = None,
) -> tuple[ApartmentCostResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            apartment_cost = db.query(RentalApartmentCost).filter(RentalApartmentCost.id == apartment_cost_id).first()
            if not apartment_cost:
                return (
                    None,
                    ApiErrorData(
                        message="Koszt mieszkania nie istnieje",
                        type_module="update_apartment_cost_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            apartment_cost.amount = new_amount
            apartment_cost.start_date = new_start_date
            apartment_cost.end_date = new_end_date
            db.flush()
            db.refresh(apartment_cost)
            return _to_apartment_cost_response(apartment_cost), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="update_apartment_cost_psql",
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
                type_module="update_apartment_cost_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def update_meter_psql(
    meter_id: str,
    new_is_master: bool,
    new_name: str | None,
    new_is_active: bool,
    db_session: Session | None = None,
) -> tuple[MeterResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            meter = db.query(RentalMeter).filter(RentalMeter.id == meter_id).first()
            if not meter:
                return (
                    None,
                    ApiErrorData(
                        message="Licznik nie istnieje",
                        type_module="update_meter_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            meter.is_master = new_is_master
            meter.name = new_name
            meter.is_active = new_is_active
            db.flush()
            db.refresh(meter)
            return _to_meter_response(meter), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="update_meter_psql",
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
                type_module="update_meter_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
