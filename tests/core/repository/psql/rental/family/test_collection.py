from datetime import date

from sqlalchemy.orm import Session

from core.repository.psql.rental.family.collection import (
    collection_allocation_rules_psql,
    collection_beneficiaries_psql,
    collection_beneficiary_settlements_psql,
)
from tests.core.repository.psql.rental.helper import (
    make_allocation_rule,
    make_apartment,
    make_beneficiary,
    make_beneficiary_settlement,
    make_beneficiary_settlement_item,
    make_billing_period,
)


class TestCollectionBeneficiariesPsql:
    def test_collection01_sorted_by_name(self, db_session: Session):
        make_beneficiary(db_session, name="Ojciec")
        make_beneficiary(db_session, name="Ja")
        make_beneficiary(db_session, name="Mama")

        result, err, ok = collection_beneficiaries_psql(db_session=db_session)

        assert ok is True and err is None
        assert [beneficiary.name for beneficiary in result] == ["Ja", "Mama", "Ojciec"]

    def test_collection02_filter_is_active(self, db_session: Session):
        make_beneficiary(db_session, name="Ja")
        make_beneficiary(db_session, name="Były wspólnik", is_active=False)

        result, err, ok = collection_beneficiaries_psql(is_active=True, db_session=db_session)

        assert ok is True
        assert [beneficiary.name for beneficiary in result] == ["Ja"]


class TestCollectionAllocationRulesPsql:
    def test_collection01_filter_by_beneficiary(self, db_session: Session):
        beneficiary = make_beneficiary(db_session, name="Ja")
        make_allocation_rule(db_session, beneficiary=beneficiary, component="electricity", mode="full", amount=None)
        make_allocation_rule(db_session)  # inny beneficjent

        result, err, ok = collection_allocation_rules_psql(beneficiary_id=str(beneficiary.id), db_session=db_session)

        assert ok is True
        assert len(result) == 1
        assert result[0].component == "electricity"

    def test_collection02_active_on_excludes_ended_rules(self, db_session: Session):
        beneficiary = make_beneficiary(db_session)
        # stawka podatku zmieniła się od czerwca 2026
        make_allocation_rule(
            db_session,
            beneficiary=beneficiary,
            component="recurring",
            amount=-270.00,
            description="podatek",
            start_date=date(2025, 1, 1),
            end_date=date(2026, 5, 31),
        )
        make_allocation_rule(
            db_session,
            beneficiary=beneficiary,
            component="recurring",
            amount=-300.00,
            description="podatek",
            start_date=date(2026, 6, 1),
        )

        result, err, ok = collection_allocation_rules_psql(
            beneficiary_id=str(beneficiary.id), active_on=date(2026, 6, 15), db_session=db_session
        )

        assert ok is True
        assert len(result) == 1
        assert result[0].amount == -300.00

    def test_collection03_filter_by_apartment(self, db_session: Session):
        apartment = make_apartment(db_session)
        make_allocation_rule(db_session, apartment=apartment)
        make_allocation_rule(db_session)  # bez mieszkania

        result, err, ok = collection_allocation_rules_psql(apartment_id=str(apartment.id), db_session=db_session)

        assert ok is True
        assert len(result) == 1


class TestCollectionBeneficiarySettlementsPsql:
    def test_collection01_by_period_with_items(self, db_session: Session):
        period = make_billing_period(db_session)
        ja = make_beneficiary_settlement(
            db_session, period=period, beneficiary=make_beneficiary(db_session, name="Ja"), total_amount=345.00
        )
        make_beneficiary_settlement(
            db_session,
            period=period,
            beneficiary=make_beneficiary(db_session, name="Ojciec"),
            total_amount=1790.00,
        )
        make_beneficiary_settlement_item(db_session, beneficiary_settlement=ja, description="podatek", amount=-90.00)

        result, err, ok = collection_beneficiary_settlements_psql(period_id=str(period.id), db_session=db_session)

        assert ok is True
        assert len(result) == 2
        by_total = {settlement.total_amount: settlement for settlement in result}
        assert by_total[345.00].items[0].description == "podatek"
        assert by_total[1790.00].items == []

    def test_collection02_by_beneficiary_history(self, db_session: Session):
        beneficiary = make_beneficiary(db_session, name="Mama")
        may = make_billing_period(db_session, period_month=date(2026, 5, 1))
        june = make_billing_period(db_session, period_month=date(2026, 6, 1))
        make_beneficiary_settlement(db_session, period=may, beneficiary=beneficiary, total_amount=822.00)
        make_beneficiary_settlement(db_session, period=june, beneficiary=beneficiary, total_amount=940.00)

        result, err, ok = collection_beneficiary_settlements_psql(
            beneficiary_id=str(beneficiary.id), db_session=db_session
        )

        assert ok is True
        assert len(result) == 2
