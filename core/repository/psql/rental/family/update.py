from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.rental.family.response import (
    AllocationRuleResponse,
    BeneficiaryResponse,
    _to_allocation_rule_response,
    _to_beneficiary_response,
)
from database.psql.database import managed_session
from database.psql.models.rentals import RentalAllocationRule, RentalBeneficiary


def update_beneficiary_psql(
    beneficiary_id: str,
    new_name: str,
    new_is_active: bool,
    db_session: Session | None = None,
) -> tuple[BeneficiaryResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            beneficiary = db.query(RentalBeneficiary).filter(RentalBeneficiary.id == beneficiary_id).first()
            if not beneficiary:
                return (
                    None,
                    ApiErrorData(
                        message="Beneficjent nie istnieje",
                        type_module="update_beneficiary_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            beneficiary.name = new_name
            beneficiary.is_active = new_is_active
            db.flush()
            db.refresh(beneficiary)
            return _to_beneficiary_response(beneficiary), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="update_beneficiary_psql",
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
                type_module="update_beneficiary_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def update_allocation_rule_psql(
    rule_id: str,
    new_apartment_id: str | None,
    new_component: str,
    new_cost_type_id: str | None,
    new_mode: str,
    new_amount: float | None,
    new_start_date: date,
    new_end_date: date | None,
    db_session: Session | None = None,
) -> tuple[AllocationRuleResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            rule = db.query(RentalAllocationRule).filter(RentalAllocationRule.id == rule_id).first()
            if not rule:
                return (
                    None,
                    ApiErrorData(
                        message="Reguła podziału nie istnieje",
                        type_module="update_allocation_rule_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            rule.apartment_id = new_apartment_id
            rule.component = new_component
            rule.cost_type_id = new_cost_type_id
            rule.mode = new_mode
            rule.amount = new_amount
            rule.start_date = new_start_date
            rule.end_date = new_end_date
            db.flush()
            db.refresh(rule)
            return _to_allocation_rule_response(rule), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="update_allocation_rule_psql",
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
                type_module="update_allocation_rule_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
