from datetime import date

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.family.response import (
    AllocationRuleResponse,
    BeneficiaryResponse,
)
from core.repository.psql.rental.family.update import (
    update_allocation_rule_psql,
    update_beneficiary_psql,
)


def handler_update_beneficiary(
    user_id: str,
    beneficiary_id: str,
    new_name: str,
    new_is_active: bool,
    db_session: Session | None = None,
) -> tuple[BeneficiaryResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_beneficiary_psql(beneficiary_id, new_name, new_is_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:update_beneficiary", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_update_beneficiary",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_update_allocation_rule(
    user_id: str,
    rule_id: str,
    new_apartment_id: str | None,
    new_component: str,
    new_cost_type_id: str | None,
    new_mode: str,
    new_amount: float | None,
    new_description: str | None,
    new_start_date: date,
    new_end_date: date | None,
    db_session: Session | None = None,
) -> tuple[AllocationRuleResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_allocation_rule_psql(
            rule_id,
            new_apartment_id,
            new_component,
            new_cost_type_id,
            new_mode,
            new_amount,
            new_description,
            new_start_date,
            new_end_date,
            db_session=db_session,
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:update_allocation_rule", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_update_allocation_rule",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
