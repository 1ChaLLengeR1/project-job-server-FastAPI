from datetime import date

from sqlalchemy.orm import Session

from core.repository.psql.rental.family.create import (
    create_allocation_rule_psql,
    create_beneficiary_psql,
    create_beneficiary_settlement_psql,
)
from core.repository.psql.rental.family.response import BeneficiarySettlementItemInput
from tests.core.repository.psql.rental.helper import (
    make_allocation_rule,
    make_apartment,
    make_beneficiary,
    make_beneficiary_settlement,
    make_billing_period,
    make_cost_type,
    make_settlement,
)


class TestCreateBeneficiaryPsql:
    def test_create01_returns_ok_with_fields(self, db_session: Session):
        result, err, ok = create_beneficiary_psql("Mama", db_session=db_session)

        assert ok is True and err is None
        assert result.name == "Mama"
        assert result.is_active is True

    def test_create02_duplicate_name_integrity_error(self, db_session: Session):
        make_beneficiary(db_session, name="Ojciec")

        result, err, ok = create_beneficiary_psql("Ojciec", db_session=db_session)

        assert ok is False
        assert err.key_type_error == "IntegrityError"


class TestCreateAllocationRulePsql:
    def test_create01_fixed_rent_rule(self, db_session: Session):
        beneficiary = make_beneficiary(db_session, name="Ojciec")
        apartment = make_apartment(db_session)

        # czynsz Dudzik -> Ojciec 1100 zł (Obliczenia_3)
        result, err, ok = create_allocation_rule_psql(
            str(beneficiary.id),
            "rent",
            "fixed_amount",
            date(2026, 1, 1),
            apartment_id=str(apartment.id),
            amount=1100.00,
            db_session=db_session,
        )

        assert ok is True and err is None
        assert result.component == "rent"
        assert result.mode == "fixed_amount"
        assert result.amount == 1100.00
        assert result.apartment_id == str(apartment.id)
        assert result.description is None

    def test_create02_recurring_with_description(self, db_session: Session):
        beneficiary = make_beneficiary(db_session, name="Ja")

        # podatek -90 zł (Obliczenia_3, sekcja "Ja")
        result, err, ok = create_allocation_rule_psql(
            str(beneficiary.id),
            "recurring",
            "fixed_amount",
            date(2026, 1, 1),
            amount=-90.00,
            description="podatek",
            db_session=db_session,
        )

        assert ok is True
        assert result.amount == -90.00
        assert result.description == "podatek"
        assert result.apartment_id is None

    def test_create03_cost_type_full_rule(self, db_session: Session):
        beneficiary = make_beneficiary(db_session, name="Mama")
        cost_type = make_cost_type(db_session, name="śmieci", charge_type="per_person")

        result, err, ok = create_allocation_rule_psql(
            str(beneficiary.id),
            "cost_type",
            "full",
            date(2026, 1, 1),
            cost_type_id=str(cost_type.id),
            db_session=db_session,
        )

        assert ok is True
        assert result.cost_type_id == str(cost_type.id)
        assert result.amount is None


class TestCreateBeneficiarySettlementPsql:
    def test_create01_creates_with_items(self, db_session: Session):
        period = make_billing_period(db_session)
        beneficiary = make_beneficiary(db_session, name="Mama")
        rule = make_allocation_rule(db_session, beneficiary=beneficiary)
        settlement = make_settlement(db_session, period=period)

        # sekcja "Mama" z Obliczenia_3: czynsz 100 + podatek 360 + media
        result, err, ok = create_beneficiary_settlement_psql(
            str(period.id),
            str(beneficiary.id),
            940.00,
            items=[
                BeneficiarySettlementItemInput(
                    "czynsz - Pokój Państwa Dudzik", 100.00, str(rule.id), str(settlement.id)
                ),
                BeneficiarySettlementItemInput("podatek", 360.00),
                BeneficiarySettlementItemInput("woda - Pokój Państwa Dudzik", 64.00, None, str(settlement.id)),
            ],
            db_session=db_session,
        )

        assert ok is True and err is None
        assert result.total_amount == 940.00
        assert len(result.items) == 3
        assert result.items[0].rule_id == str(rule.id)
        assert result.items[1].rule_id is None

    def test_create02_duplicate_period_beneficiary_integrity_error(self, db_session: Session):
        period = make_billing_period(db_session)
        beneficiary = make_beneficiary(db_session)
        make_beneficiary_settlement(db_session, period=period, beneficiary=beneficiary)

        result, err, ok = create_beneficiary_settlement_psql(
            str(period.id), str(beneficiary.id), 0, items=[], db_session=db_session
        )

        assert ok is False
        assert err.key_type_error == "IntegrityError"
