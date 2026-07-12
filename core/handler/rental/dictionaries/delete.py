from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.dictionaries.delete import (
    delete_apartment_cost_psql,
    delete_apartment_psql,
    delete_cost_type_psql,
    delete_meter_psql,
    delete_tenancy_psql,
    delete_tenant_psql,
)
from core.repository.psql.rental.dictionaries.response import (
    ApartmentCostResponse,
    ApartmentResponse,
    CostTypeResponse,
    MeterResponse,
    TenancyResponse,
    TenantResponse,
)


def handler_delete_apartment(
    user_id: str, apartment_id: str, db_session: Session | None = None
) -> tuple[ApartmentResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = delete_apartment_psql(apartment_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:delete_apartment", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_delete_apartment",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_delete_tenant(
    user_id: str, tenant_id: str, db_session: Session | None = None
) -> tuple[TenantResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = delete_tenant_psql(tenant_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:delete_tenant", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_delete_tenant",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_delete_tenancy(
    user_id: str, tenancy_id: str, db_session: Session | None = None
) -> tuple[TenancyResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = delete_tenancy_psql(tenancy_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:delete_tenancy", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_delete_tenancy",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_delete_cost_type(
    user_id: str, cost_type_id: str, db_session: Session | None = None
) -> tuple[CostTypeResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = delete_cost_type_psql(cost_type_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:delete_cost_type", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_delete_cost_type",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_delete_apartment_cost(
    user_id: str, apartment_cost_id: str, db_session: Session | None = None
) -> tuple[ApartmentCostResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = delete_apartment_cost_psql(apartment_cost_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:delete_apartment_cost", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_delete_apartment_cost",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_delete_meter(
    user_id: str, meter_id: str, db_session: Session | None = None
) -> tuple[MeterResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = delete_meter_psql(meter_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:delete_meter", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_delete_meter",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
