from datetime import date

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.family.create import (
    create_allocation_rule_psql,
    create_beneficiary_psql,
)
from core.repository.psql.rental.family.response import (
    AllocationRuleResponse,
    BeneficiaryResponse,
)


def handler_create_beneficiary(
    user_id: str,
    name: str,
    is_active: bool = True,
    db_session: Session | None = None,
) -> tuple[BeneficiaryResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = create_beneficiary_psql(name, is_active, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:create_beneficiary", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_create_beneficiary",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_create_allocation_rule(
    user_id: str,
    beneficiary_id: str,
    component: str,
    mode: str,
    start_date: date,
    apartment_id: str | None = None,
    cost_type_id: str | None = None,
    amount: float | None = None,
    description: str | None = None,
    end_date: date | None = None,
    db_session: Session | None = None,
) -> tuple[AllocationRuleResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = create_allocation_rule_psql(
            beneficiary_id,
            component,
            mode,
            start_date,
            apartment_id=apartment_id,
            cost_type_id=cost_type_id,
            amount=amount,
            description=description,
            end_date=end_date,
            db_session=db_session,
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:create_allocation_rule", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_create_allocation_rule",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
