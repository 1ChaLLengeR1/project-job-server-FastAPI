from datetime import date

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.dictionaries.collection import (
    collection_apartment_costs_psql,
    collection_apartments_psql,
    collection_cost_types_psql,
    collection_meters_psql,
    collection_tenancies_psql,
    collection_tenants_psql,
)
from core.repository.psql.rental.dictionaries.response import (
    ApartmentCostResponse,
    ApartmentResponse,
    CostTypeResponse,
    MeterResponse,
    TenancyResponse,
    TenantResponse,
)


def handler_collection_apartments(
    user_id: str, is_active: bool | None = None, db_session: Session | None = None
) -> tuple[list[ApartmentResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_apartments_psql(is_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:collection_apartments", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_apartments",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_collection_tenants(
    user_id: str, is_active: bool | None = None, db_session: Session | None = None
) -> tuple[list[TenantResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_tenants_psql(is_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:collection_tenants", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_tenants",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_collection_tenancies(
    user_id: str,
    apartment_id: str | None = None,
    tenant_id: str | None = None,
    active_on: date | None = None,
    db_session: Session | None = None,
) -> tuple[list[TenancyResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_tenancies_psql(apartment_id, tenant_id, active_on, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:collection_tenancies", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_tenancies",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_collection_cost_types(
    user_id: str, is_active: bool | None = None, db_session: Session | None = None
) -> tuple[list[CostTypeResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_cost_types_psql(is_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:collection_cost_types", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_cost_types",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_collection_apartment_costs(
    user_id: str,
    apartment_id: str | None = None,
    active_on: date | None = None,
    db_session: Session | None = None,
) -> tuple[list[ApartmentCostResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_apartment_costs_psql(apartment_id, active_on, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:collection_apartment_costs", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_apartment_costs",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_collection_meters(
    user_id: str,
    apartment_id: str | None = None,
    media_type: str | None = None,
    is_active: bool | None = None,
    db_session: Session | None = None,
) -> tuple[list[MeterResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_meters_psql(apartment_id, media_type, is_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:collection_meters", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_meters",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
