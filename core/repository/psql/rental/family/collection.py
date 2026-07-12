from datetime import date

from sqlalchemy import or_
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.rental.family.response import (
    AllocationRuleResponse,
    BeneficiaryResponse,
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


def collection_beneficiaries_psql(
    is_active: bool | None = None, db_session: Session | None = None
) -> tuple[list[BeneficiaryResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(RentalBeneficiary)
            if is_active is not None:
                query = query.filter(RentalBeneficiary.is_active == is_active)
            beneficiaries = query.order_by(RentalBeneficiary.name.asc()).all()
            return [_to_beneficiary_response(beneficiary) for beneficiary in beneficiaries], None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_beneficiaries_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def collection_allocation_rules_psql(
    beneficiary_id: str | None = None,
    apartment_id: str | None = None,
    active_on: date | None = None,
    db_session: Session | None = None,
) -> tuple[list[AllocationRuleResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(RentalAllocationRule)
            if beneficiary_id is not None:
                query = query.filter(RentalAllocationRule.beneficiary_id == beneficiary_id)
            if apartment_id is not None:
                query = query.filter(RentalAllocationRule.apartment_id == apartment_id)
            if active_on is not None:
                query = query.filter(RentalAllocationRule.start_date <= active_on).filter(
                    or_(RentalAllocationRule.end_date.is_(None), RentalAllocationRule.end_date >= active_on)
                )
            rules = query.order_by(RentalAllocationRule.created_at.asc()).all()
            return [_to_allocation_rule_response(rule) for rule in rules], None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_allocation_rules_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def collection_beneficiary_settlements_psql(
    period_id: str | None = None,
    beneficiary_id: str | None = None,
    db_session: Session | None = None,
) -> tuple[list[BeneficiarySettlementResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(RentalBeneficiarySettlement)
            if period_id is not None:
                query = query.filter(RentalBeneficiarySettlement.period_id == period_id)
            if beneficiary_id is not None:
                query = query.filter(RentalBeneficiarySettlement.beneficiary_id == beneficiary_id)
            settlements = query.order_by(RentalBeneficiarySettlement.created_at.asc()).all()

            settlement_ids = [settlement.id for settlement in settlements]
            items_by_settlement: dict = {}
            if settlement_ids:
                items = (
                    db.query(RentalBeneficiarySettlementItem)
                    .filter(RentalBeneficiarySettlementItem.beneficiary_settlement_id.in_(settlement_ids))
                    .order_by(RentalBeneficiarySettlementItem.created_at.asc())
                    .all()
                )
                for item in items:
                    items_by_settlement.setdefault(item.beneficiary_settlement_id, []).append(item)

            return (
                [
                    _to_beneficiary_settlement_response(settlement, items_by_settlement.get(settlement.id, []))
                    for settlement in settlements
                ],
                None,
                True,
            )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_beneficiary_settlements_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
