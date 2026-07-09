from datetime import date

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.dictionaries.create import (
    create_apartment_cost_psql,
    create_apartment_psql,
    create_cost_type_psql,
    create_meter_psql,
    create_tenancy_psql,
    create_tenant_psql,
)
from core.repository.psql.rental.dictionaries.response import (
    ApartmentCostResponse,
    ApartmentResponse,
    CostTypeResponse,
    MeterResponse,
    TenancyResponse,
    TenantResponse,
)


def handler_create_apartment(
    user_id: str,
    name: str,
    description: str | None = None,
    is_active: bool = True,
    db_session: Session | None = None,
) -> tuple[ApartmentResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = create_apartment_psql(name, description, is_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:create_apartment", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_create_apartment",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_create_tenant(
    user_id: str,
    first_name: str,
    last_name: str | None = None,
    note: str | None = None,
    is_active: bool = True,
    db_session: Session | None = None,
) -> tuple[TenantResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = create_tenant_psql(first_name, last_name, note, is_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:create_tenant", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_create_tenant",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_create_tenancy(
    user_id: str,
    apartment_id: str,
    tenant_id: str,
    rent_amount: float,
    persons_count: int,
    start_date: date,
    end_date: date | None = None,
    db_session: Session | None = None,
) -> tuple[TenancyResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = create_tenancy_psql(
            apartment_id, tenant_id, rent_amount, persons_count, start_date, end_date, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:create_tenancy", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_create_tenancy",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_create_cost_type(
    user_id: str,
    name: str,
    charge_type: str,
    is_active: bool = True,
    db_session: Session | None = None,
) -> tuple[CostTypeResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = create_cost_type_psql(name, charge_type, is_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:create_cost_type", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_create_cost_type",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_create_apartment_cost(
    user_id: str,
    apartment_id: str,
    cost_type_id: str,
    amount: float,
    start_date: date,
    end_date: date | None = None,
    db_session: Session | None = None,
) -> tuple[ApartmentCostResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = create_apartment_cost_psql(
            apartment_id, cost_type_id, amount, start_date, end_date, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:create_apartment_cost", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_create_apartment_cost",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_create_meter(
    user_id: str,
    media_type: str,
    apartment_id: str | None = None,
    is_master: bool = False,
    name: str | None = None,
    is_active: bool = True,
    db_session: Session | None = None,
) -> tuple[MeterResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = create_meter_psql(media_type, apartment_id, is_master, name, is_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:create_meter", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_create_meter",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
