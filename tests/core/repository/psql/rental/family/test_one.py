from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.rental.family.one import one_allocation_rule_psql, one_beneficiary_psql
from tests.core.repository.psql.rental.helper import make_allocation_rule, make_beneficiary


class TestOneBeneficiaryPsql:
    def test_one01_returns_beneficiary(self, db_session: Session):
        beneficiary = make_beneficiary(db_session, name="Ja")

        result, err, ok = one_beneficiary_psql(str(beneficiary.id), db_session=db_session)

        assert ok is True and err is None
        assert result.name == "Ja"

    def test_one02_not_found(self, db_session: Session):
        result, err, ok = one_beneficiary_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestOneAllocationRulePsql:
    def test_one01_returns_rule(self, db_session: Session):
        rule = make_allocation_rule(db_session, amount=1100.00, description="czynsz Dudzik")

        result, err, ok = one_allocation_rule_psql(str(rule.id), db_session=db_session)

        assert ok is True
        assert result.amount == 1100.00
        assert result.description == "czynsz Dudzik"

    def test_one02_not_found(self, db_session: Session):
        result, err, ok = one_allocation_rule_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"
