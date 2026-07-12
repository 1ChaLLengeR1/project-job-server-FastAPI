from datetime import date
from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.rental.family.update import (
    update_allocation_rule_psql,
    update_beneficiary_psql,
)
from tests.core.repository.psql.rental.helper import (
    make_allocation_rule,
    make_apartment,
    make_beneficiary,
)


class TestUpdateBeneficiaryPsql:
    def test_update01_updates_fields(self, db_session: Session):
        beneficiary = make_beneficiary(db_session, name="Tata")

        result, err, ok = update_beneficiary_psql(str(beneficiary.id), "Ojciec", True, db_session=db_session)

        assert ok is True and err is None
        assert result.name == "Ojciec"

    def test_update02_not_found(self, db_session: Session):
        result, err, ok = update_beneficiary_psql(str(uuid4()), "X", True, db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"

    def test_update03_duplicate_name_integrity_error(self, db_session: Session):
        make_beneficiary(db_session, name="Mama")
        beneficiary = make_beneficiary(db_session, name="Ja")

        result, err, ok = update_beneficiary_psql(str(beneficiary.id), "Mama", True, db_session=db_session)

        assert ok is False
        assert err.key_type_error == "IntegrityError"


class TestUpdateAllocationRulePsql:
    def test_update01_updates_amount_and_description(self, db_session: Session):
        apartment = make_apartment(db_session)
        rule = make_allocation_rule(db_session, apartment=apartment, amount=1000.00)

        # podwyżka czynszu Witka: 1000 -> 1100
        result, err, ok = update_allocation_rule_psql(
            str(rule.id),
            str(apartment.id),
            "rent",
            None,
            "fixed_amount",
            1100.00,
            "czynsz Witek",
            date(2026, 6, 1),
            None,
            db_session=db_session,
        )

        assert ok is True and err is None
        assert result.amount == 1100.00
        assert result.description == "czynsz Witek"
        assert result.start_date == date(2026, 6, 1)

    def test_update02_close_rule_sets_end_date(self, db_session: Session):
        rule = make_allocation_rule(db_session, start_date=date(2025, 1, 1))

        result, err, ok = update_allocation_rule_psql(
            str(rule.id),
            None,
            "rent",
            None,
            "fixed_amount",
            1100.00,
            None,
            date(2025, 1, 1),
            date(2026, 5, 31),
            db_session=db_session,
        )

        assert ok is True
        assert result.end_date == date(2026, 5, 31)

    def test_update03_not_found(self, db_session: Session):
        result, err, ok = update_allocation_rule_psql(
            str(uuid4()), None, "rent", None, "full", None, None, date(2026, 1, 1), None, db_session=db_session
        )

        assert ok is False
        assert err.key_type_error == "NotFound"
