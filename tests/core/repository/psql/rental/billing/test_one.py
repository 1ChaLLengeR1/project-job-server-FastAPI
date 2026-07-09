from datetime import date
from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.rental.billing.one import (
    one_billing_period_by_month_psql,
    one_billing_period_psql,
    one_last_meter_reading_psql,
    one_meter_reading_psql,
    one_settlement_psql,
)
from tests.core.repository.psql.rental.helper import (
    make_billing_period,
    make_meter,
    make_meter_reading,
    make_settlement,
    make_settlement_item,
)


class TestOneBillingPeriodPsql:
    def test_one01_returns_period(self, db_session: Session):
        period = make_billing_period(db_session, electricity_bill_amount=899.48)

        result, err, ok = one_billing_period_psql(str(period.id), db_session=db_session)

        assert ok is True and err is None
        assert result.electricity_bill_amount == 899.48

    def test_one02_not_found(self, db_session: Session):
        result, err, ok = one_billing_period_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestOneBillingPeriodByMonthPsql:
    def test_one01_finds_by_any_day_of_month(self, db_session: Session):
        period = make_billing_period(db_session, period_month=date(2026, 6, 1))

        result, err, ok = one_billing_period_by_month_psql(date(2026, 6, 25), db_session=db_session)

        assert ok is True
        assert result.id == str(period.id)

    def test_one02_not_found_for_other_month(self, db_session: Session):
        make_billing_period(db_session, period_month=date(2026, 6, 1))

        result, err, ok = one_billing_period_by_month_psql(date(2026, 7, 1), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestOneMeterReadingPsql:
    def test_one01_returns_reading(self, db_session: Session):
        reading = make_meter_reading(db_session, previous_value=5245.77, current_value=5330.12)

        result, err, ok = one_meter_reading_psql(str(reading.id), db_session=db_session)

        assert ok is True
        assert result.previous_value == 5245.77
        assert result.current_value == 5330.12

    def test_one02_not_found(self, db_session: Session):
        result, err, ok = one_meter_reading_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestOneLastMeterReadingPsql:
    def test_one01_returns_latest_by_period_month(self, db_session: Session):
        meter = make_meter(db_session)
        may = make_billing_period(db_session, period_month=date(2026, 5, 1))
        june = make_billing_period(db_session, period_month=date(2026, 6, 1))
        make_meter_reading(db_session, period=may, meter=meter, previous_value=5245.77, current_value=5330.12)
        make_meter_reading(db_session, period=june, meter=meter, previous_value=5330.12, current_value=5445.30)

        result, err, ok = one_last_meter_reading_psql(str(meter.id), db_session=db_session)

        assert ok is True
        # prefill "Ostatnio" nowego okresu = "Teraz" czerwca
        assert result.current_value == 5445.30

    def test_one02_no_readings_not_found(self, db_session: Session):
        meter = make_meter(db_session)

        result, err, ok = one_last_meter_reading_psql(str(meter.id), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestOneSettlementPsql:
    def test_one01_returns_settlement_with_items(self, db_session: Session):
        settlement = make_settlement(db_session)
        make_settlement_item(db_session, settlement=settlement, name="internet", amount=60.00)
        make_settlement_item(db_session, settlement=settlement, name="garaż", amount=200.00)

        result, err, ok = one_settlement_psql(str(settlement.id), db_session=db_session)

        assert ok is True
        assert result.electricity_cost == 335.00
        assert len(result.items) == 2
        assert {item.name for item in result.items} == {"internet", "garaż"}

    def test_one02_not_found(self, db_session: Session):
        result, err, ok = one_settlement_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"
