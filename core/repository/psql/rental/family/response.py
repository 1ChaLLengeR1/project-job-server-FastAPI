from dataclasses import dataclass, field
from datetime import date, datetime

from database.psql.models.rentals import (
    RentalAllocationRule,
    RentalBeneficiary,
    RentalBeneficiarySettlement,
    RentalBeneficiarySettlementItem,
)


@dataclass
class BeneficiaryResponse:
    id: str
    name: str
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class AllocationRuleResponse:
    id: str
    beneficiary_id: str
    apartment_id: str | None
    component: str
    cost_type_id: str | None
    mode: str
    amount: float | None
    description: str | None
    start_date: date
    end_date: date | None
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class BeneficiarySettlementItemResponse:
    id: str
    beneficiary_settlement_id: str
    description: str
    amount: float
    rule_id: str | None
    settlement_id: str | None
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class BeneficiarySettlementResponse:
    id: str
    period_id: str
    beneficiary_id: str
    total_amount: float
    created_at: datetime | None
    updated_at: datetime | None
    items: list[BeneficiarySettlementItemResponse] = field(default_factory=list)


@dataclass
class BeneficiarySettlementItemInput:
    """Dane wejściowe pozycji podziału rodzinnego przy tworzeniu snapshotu."""

    description: str
    amount: float
    rule_id: str | None = None
    settlement_id: str | None = None


def _to_beneficiary_response(model: RentalBeneficiary) -> BeneficiaryResponse:
    return BeneficiaryResponse(
        id=str(model.id),
        name=model.name,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_allocation_rule_response(model: RentalAllocationRule) -> AllocationRuleResponse:
    return AllocationRuleResponse(
        id=str(model.id),
        beneficiary_id=str(model.beneficiary_id),
        apartment_id=str(model.apartment_id) if model.apartment_id else None,
        component=model.component,
        cost_type_id=str(model.cost_type_id) if model.cost_type_id else None,
        mode=model.mode,
        amount=float(model.amount) if model.amount is not None else None,
        description=model.description,
        start_date=model.start_date,
        end_date=model.end_date,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_beneficiary_settlement_item_response(
    model: RentalBeneficiarySettlementItem,
) -> BeneficiarySettlementItemResponse:
    return BeneficiarySettlementItemResponse(
        id=str(model.id),
        beneficiary_settlement_id=str(model.beneficiary_settlement_id),
        description=model.description,
        amount=float(model.amount),
        rule_id=str(model.rule_id) if model.rule_id else None,
        settlement_id=str(model.settlement_id) if model.settlement_id else None,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _to_beneficiary_settlement_response(
    model: RentalBeneficiarySettlement, items: list[RentalBeneficiarySettlementItem] | None = None
) -> BeneficiarySettlementResponse:
    return BeneficiarySettlementResponse(
        id=str(model.id),
        period_id=str(model.period_id),
        beneficiary_id=str(model.beneficiary_id),
        total_amount=float(model.total_amount),
        created_at=model.created_at,
        updated_at=model.updated_at,
        items=[_to_beneficiary_settlement_item_response(item) for item in (items or [])],
    )
