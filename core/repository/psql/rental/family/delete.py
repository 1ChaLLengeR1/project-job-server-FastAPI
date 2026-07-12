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


def delete_beneficiary_psql(
    beneficiary_id: str, db_session: Session | None = None
) -> tuple[BeneficiaryResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            beneficiary = db.query(RentalBeneficiary).filter(RentalBeneficiary.id == beneficiary_id).first()
            if not beneficiary:
                return (
                    None,
                    ApiErrorData(
                        message="Beneficjent nie istnieje",
                        type_module="delete_beneficiary_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            deleted_beneficiary = _to_beneficiary_response(beneficiary)
            db.delete(beneficiary)
            db.flush()
            return deleted_beneficiary, None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="delete_beneficiary_psql",
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
                type_module="delete_beneficiary_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def delete_allocation_rule_psql(
    rule_id: str, db_session: Session | None = None
) -> tuple[AllocationRuleResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            rule = db.query(RentalAllocationRule).filter(RentalAllocationRule.id == rule_id).first()
            if not rule:
                return (
                    None,
                    ApiErrorData(
                        message="Reguła podziału nie istnieje",
                        type_module="delete_allocation_rule_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            deleted_rule = _to_allocation_rule_response(rule)
            db.delete(rule)
            db.flush()
            return deleted_rule, None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="delete_allocation_rule_psql",
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
                type_module="delete_allocation_rule_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
