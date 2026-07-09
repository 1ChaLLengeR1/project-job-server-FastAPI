from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.rental.family.delete import (
    delete_allocation_rule_psql,
    delete_beneficiary_psql,
)
from database.psql.models.rentals import RentalAllocationRule, RentalBeneficiary
from tests.core.repository.psql.rental.helper import make_allocation_rule, make_beneficiary


class TestDeleteBeneficiaryPsql:
    def test_delete01_deletes(self, db_session: Session):
        beneficiary = make_beneficiary(db_session, name="Były wspólnik")

        result, err, ok = delete_beneficiary_psql(str(beneficiary.id), db_session=db_session)

        assert ok is True and err is None
        assert result.name == "Były wspólnik"
        assert db_session.query(RentalBeneficiary).count() == 0

    def test_delete02_restrict_blocks_with_rule(self, db_session: Session):
        beneficiary = make_beneficiary(db_session)
        make_allocation_rule(db_session, beneficiary=beneficiary)

        result, err, ok = delete_beneficiary_psql(str(beneficiary.id), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "IntegrityError"

    def test_delete03_not_found(self, db_session: Session):
        result, err, ok = delete_beneficiary_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestDeleteAllocationRulePsql:
    def test_delete01_deletes(self, db_session: Session):
        rule = make_allocation_rule(db_session)

        result, err, ok = delete_allocation_rule_psql(str(rule.id), db_session=db_session)

        assert ok is True
        assert db_session.query(RentalAllocationRule).count() == 0

    def test_delete02_not_found(self, db_session: Session):
        result, err, ok = delete_allocation_rule_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"
