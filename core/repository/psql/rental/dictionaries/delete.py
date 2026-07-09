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


def delete_apartment_psql(
    apartment_id: str, db_session: Session | None = None
) -> tuple[ApartmentResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            apartment = db.query(RentalApartment).filter(RentalApartment.id == apartment_id).first()
            if not apartment:
                return (
                    None,
                    ApiErrorData(
                        message="Mieszkanie nie istnieje",
                        type_module="delete_apartment_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            deleted_apartment = _to_apartment_response(apartment)
            db.delete(apartment)
            db.flush()
            return deleted_apartment, None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="delete_apartment_psql",
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
                type_module="delete_apartment_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def delete_tenant_psql(
    tenant_id: str, db_session: Session | None = None
) -> tuple[TenantResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            tenant = db.query(RentalTenant).filter(RentalTenant.id == tenant_id).first()
            if not tenant:
                return (
                    None,
                    ApiErrorData(
                        message="Najemca nie istnieje",
                        type_module="delete_tenant_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            deleted_tenant = _to_tenant_response(tenant)
            db.delete(tenant)
            db.flush()
            return deleted_tenant, None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="delete_tenant_psql",
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
                type_module="delete_tenant_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def delete_tenancy_psql(
    tenancy_id: str, db_session: Session | None = None
) -> tuple[TenancyResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            tenancy = db.query(RentalTenancy).filter(RentalTenancy.id == tenancy_id).first()
            if not tenancy:
                return (
                    None,
                    ApiErrorData(
                        message="Najem nie istnieje",
                        type_module="delete_tenancy_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            deleted_tenancy = _to_tenancy_response(tenancy)
            db.delete(tenancy)
            db.flush()
            return deleted_tenancy, None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="delete_tenancy_psql",
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
                type_module="delete_tenancy_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def delete_cost_type_psql(
    cost_type_id: str, db_session: Session | None = None
) -> tuple[CostTypeResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            cost_type = db.query(RentalCostType).filter(RentalCostType.id == cost_type_id).first()
            if not cost_type:
                return (
                    None,
                    ApiErrorData(
                        message="Rodzaj kosztu nie istnieje",
                        type_module="delete_cost_type_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            deleted_cost_type = _to_cost_type_response(cost_type)
            db.delete(cost_type)
            db.flush()
            return deleted_cost_type, None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="delete_cost_type_psql",
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
                type_module="delete_cost_type_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def delete_apartment_cost_psql(
    apartment_cost_id: str, db_session: Session | None = None
) -> tuple[ApartmentCostResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            apartment_cost = db.query(RentalApartmentCost).filter(RentalApartmentCost.id == apartment_cost_id).first()
            if not apartment_cost:
                return (
                    None,
                    ApiErrorData(
                        message="Koszt mieszkania nie istnieje",
                        type_module="delete_apartment_cost_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            deleted_apartment_cost = _to_apartment_cost_response(apartment_cost)
            db.delete(apartment_cost)
            db.flush()
            return deleted_apartment_cost, None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="delete_apartment_cost_psql",
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
                type_module="delete_apartment_cost_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def delete_meter_psql(
    meter_id: str, db_session: Session | None = None
) -> tuple[MeterResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            meter = db.query(RentalMeter).filter(RentalMeter.id == meter_id).first()
            if not meter:
                return (
                    None,
                    ApiErrorData(
                        message="Licznik nie istnieje",
                        type_module="delete_meter_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            deleted_meter = _to_meter_response(meter)
            db.delete(meter)
            db.flush()
            return deleted_meter, None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="delete_meter_psql",
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
                type_module="delete_meter_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
