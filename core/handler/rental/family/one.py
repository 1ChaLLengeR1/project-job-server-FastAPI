from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.family.one import one_allocation_rule_psql, one_beneficiary_psql
from core.repository.psql.rental.family.response import (
    AllocationRuleResponse,
    BeneficiaryResponse,
)


def handler_one_beneficiary(
    user_id: str, beneficiary_id: str, db_session: Session | None = None
) -> tuple[BeneficiaryResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = one_beneficiary_psql(beneficiary_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:one_beneficiary", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_one_beneficiary",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_one_allocation_rule(
    user_id: str, rule_id: str, db_session: Session | None = None
) -> tuple[AllocationRuleResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = one_allocation_rule_psql(rule_id, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:one_allocation_rule", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_one_allocation_rule",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
