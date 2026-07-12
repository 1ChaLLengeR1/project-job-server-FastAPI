from datetime import date

from sqlalchemy.orm import Session

from core.repository.psql.rental.billing.collection import (
    collection_billing_periods_psql,
    collection_meter_readings_psql,
    collection_settlements_psql,
)
from tests.core.repository.psql.rental.helper import (
    make_apartment,
    make_billing_period,
    make_meter,
    make_meter_reading,
    make_settlement,
    make_settlement_item,
)


class TestCollectionBillingPeriodsPsql:
    def test_collection01_sorted_by_month_desc(self, db_session: Session):
        make_billing_period(db_session, period_month=date(2026, 5, 1))
        make_billing_period(db_session, period_month=date(2026, 7, 1))
        make_billing_period(db_session, period_month=date(2026, 6, 1))

        result, err, ok = collection_billing_periods_psql(db_session=db_session)

        assert ok is True and err is None
        assert [period.period_month for period in result] == [
            date(2026, 7, 1),
            date(2026, 6, 1),
            date(2026, 5, 1),
        ]

    def test_collection02_filter_status(self, db_session: Session):
        make_billing_period(db_session, period_month=date(2026, 5, 1), status="closed")
        make_billing_period(db_session, period_month=date(2026, 6, 1), status="draft")

        result, err, ok = collection_billing_periods_psql(status="draft", db_session=db_session)

        assert ok is True
        assert len(result) == 1
        assert result[0].status == "draft"


class TestCollectionMeterReadingsPsql:
    def test_collection01_returns_readings_of_period(self, db_session: Session):
        period = make_billing_period(db_session)
        other_period = make_billing_period(db_session, period_month=date(2026, 7, 1))
        make_meter_reading(db_session, period=period, meter=make_meter(db_session))
        make_meter_reading(db_session, period=period, meter=make_meter(db_session))
        make_meter_reading(db_session, period=other_period, meter=make_meter(db_session))

        result, err, ok = collection_meter_readings_psql(str(period.id), db_session=db_session)

        assert ok is True
        assert len(result) == 2

    def test_collection02_empty(self, db_session: Session):
        period = make_billing_period(db_session)

        result, err, ok = collection_meter_readings_psql(str(period.id), db_session=db_session)

        assert ok is True
        assert result == []


class TestCollectionSettlementsPsql:
    def test_collection01_by_period_with_items(self, db_session: Session):
        period = make_billing_period(db_session)
        settlement_a = make_settlement(db_session, period=period)
        settlement_b = make_settlement(db_session, period=period, apartment=make_apartment(db_session))
        make_settlement_item(db_session, settlement=settlement_a, name="internet", amount=60.00)
        make_settlement_item(db_session, settlement=settlement_b, name="śmieci", amount=27.00)

        result, err, ok = collection_settlements_psql(period_id=str(period.id), db_session=db_session)

        assert ok is True
        assert len(result) == 2
        items_by_id = {settlement.id: settlement.items for settlement in result}
        assert len(items_by_id[str(settlement_a.id)]) == 1
        assert items_by_id[str(settlement_a.id)][0].name == "internet"
        assert items_by_id[str(settlement_b.id)][0].name == "śmieci"

    def test_collection02_by_apartment_history(self, db_session: Session):
        apartment = make_apartment(db_session)
        may = make_billing_period(db_session, period_month=date(2026, 5, 1))
        june = make_billing_period(db_session, period_month=date(2026, 6, 1))
        make_settlement(db_session, period=may, apartment=apartment)
        make_settlement(db_session, period=june, apartment=apartment)
        make_settlement(db_session, period=june)  # inne mieszkanie

        result, err, ok = collection_settlements_psql(apartment_id=str(apartment.id), db_session=db_session)

        assert ok is True
        assert len(result) == 2
