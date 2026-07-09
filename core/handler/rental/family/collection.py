from datetime import date

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.family.collection import (
    collection_allocation_rules_psql,
    collection_beneficiaries_psql,
    collection_beneficiary_settlements_psql,
)
from core.repository.psql.rental.family.response import (
    AllocationRuleResponse,
    BeneficiaryResponse,
    BeneficiarySettlementResponse,
)


def handler_collection_beneficiaries(
    user_id: str, is_active: bool | None = None, db_session: Session | None = None
) -> tuple[list[BeneficiaryResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_beneficiaries_psql(is_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:collection_beneficiaries", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_beneficiaries",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_collection_allocation_rules(
    user_id: str,
    beneficiary_id: str | None = None,
    apartment_id: str | None = None,
    active_on: date | None = None,
    db_session: Session | None = None,
) -> tuple[list[AllocationRuleResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_allocation_rules_psql(
            beneficiary_id, apartment_id, active_on, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:collection_allocation_rules", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_allocation_rules",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_collection_beneficiary_settlements(
    user_id: str,
    period_id: str | None = None,
    beneficiary_id: str | None = None,
    db_session: Session | None = None,
) -> tuple[list[BeneficiarySettlementResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_beneficiary_settlements_psql(period_id, beneficiary_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:collection_beneficiary_settlements", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_collection_beneficiary_settlements",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
