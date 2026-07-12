from datetime import date

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.dictionaries.response import (
    ApartmentCostResponse,
    ApartmentResponse,
    CostTypeResponse,
    MeterResponse,
    TenancyResponse,
    TenantResponse,
)
from core.repository.psql.rental.dictionaries.update import (
    update_apartment_cost_psql,
    update_apartment_psql,
    update_cost_type_psql,
    update_meter_psql,
    update_tenancy_psql,
    update_tenant_psql,
)


def handler_update_apartment(
    user_id: str,
    apartment_id: str,
    new_name: str,
    new_description: str | None,
    new_is_active: bool,
    db_session: Session | None = None,
) -> tuple[ApartmentResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_apartment_psql(
            apartment_id, new_name, new_description, new_is_active, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:update_apartment", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_update_apartment",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_update_tenant(
    user_id: str,
    tenant_id: str,
    new_first_name: str,
    new_last_name: str | None,
    new_note: str | None,
    new_is_active: bool,
    db_session: Session | None = None,
) -> tuple[TenantResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_tenant_psql(
            tenant_id, new_first_name, new_last_name, new_note, new_is_active, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:update_tenant", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_update_tenant",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_update_tenancy(
    user_id: str,
    tenancy_id: str,
    new_rent_amount: float,
    new_persons_count: int,
    new_start_date: date,
    new_end_date: date | None,
    db_session: Session | None = None,
) -> tuple[TenancyResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_tenancy_psql(
            tenancy_id, new_rent_amount, new_persons_count, new_start_date, new_end_date, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:update_tenancy", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_update_tenancy",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_update_cost_type(
    user_id: str,
    cost_type_id: str,
    new_name: str,
    new_charge_type: str,
    new_is_active: bool,
    db_session: Session | None = None,
) -> tuple[CostTypeResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_cost_type_psql(
            cost_type_id, new_name, new_charge_type, new_is_active, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:update_cost_type", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_update_cost_type",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_update_apartment_cost(
    user_id: str,
    apartment_cost_id: str,
    new_amount: float,
    new_start_date: date,
    new_end_date: date | None,
    db_session: Session | None = None,
) -> tuple[ApartmentCostResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_apartment_cost_psql(
            apartment_cost_id, new_amount, new_start_date, new_end_date, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:update_apartment_cost", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_update_apartment_cost",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_update_meter(
    user_id: str,
    meter_id: str,
    new_is_master: bool,
    new_name: str | None,
    new_is_active: bool,
    db_session: Session | None = None,
) -> tuple[MeterResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_meter_psql(meter_id, new_is_master, new_name, new_is_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:update_meter", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_update_meter",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
