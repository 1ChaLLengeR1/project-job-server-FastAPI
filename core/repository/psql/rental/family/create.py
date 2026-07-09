from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.rental.family.response import (
    AllocationRuleResponse,
    BeneficiaryResponse,
    BeneficiarySettlementItemInput,
    BeneficiarySettlementResponse,
    _to_allocation_rule_response,
    _to_beneficiary_response,
    _to_beneficiary_settlement_response,
)
from database.psql.database import managed_session
from database.psql.models.rentals import (
    RentalAllocationRule,
    RentalBeneficiary,
    RentalBeneficiarySettlement,
    RentalBeneficiarySettlementItem,
)


def create_beneficiary_psql(
    name: str, is_active: bool = True, db_session: Session | None = None
) -> tuple[BeneficiaryResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_beneficiary = RentalBeneficiary(name=name, is_active=is_active)
            db.add(new_beneficiary)
            db.flush()
            db.refresh(new_beneficiary)
            return _to_beneficiary_response(new_beneficiary), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_beneficiary_psql",
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
                type_module="create_beneficiary_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def create_allocation_rule_psql(
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
        with managed_session(db_session) as (db, _):
            new_rule = RentalAllocationRule(
                beneficiary_id=beneficiary_id,
                apartment_id=apartment_id,
                component=component,
                cost_type_id=cost_type_id,
                mode=mode,
                amount=amount,
                description=description,
                start_date=start_date,
                end_date=end_date,
            )
            db.add(new_rule)
            db.flush()
            db.refresh(new_rule)
            return _to_allocation_rule_response(new_rule), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_allocation_rule_psql",
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
                type_module="create_allocation_rule_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def create_beneficiary_settlement_psql(
    period_id: str,
    beneficiary_id: str,
    total_amount: float,
    items: list[BeneficiarySettlementItemInput],
    db_session: Session | None = None,
) -> tuple[BeneficiarySettlementResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_settlement = RentalBeneficiarySettlement(
                period_id=period_id,
                beneficiary_id=beneficiary_id,
                total_amount=total_amount,
            )
            db.add(new_settlement)
            db.flush()

            new_items = []
            for item in items:
                new_item = RentalBeneficiarySettlementItem(
                    beneficiary_settlement_id=new_settlement.id,
                    description=item.description,
                    amount=item.amount,
                    rule_id=item.rule_id,
                    settlement_id=item.settlement_id,
                )
                db.add(new_item)
                new_items.append(new_item)
            db.flush()

            db.refresh(new_settlement)
            for new_item in new_items:
                db.refresh(new_item)
            return _to_beneficiary_settlement_response(new_settlement, new_items), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="create_beneficiary_settlement_psql",
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
                type_module="create_beneficiary_settlement_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
