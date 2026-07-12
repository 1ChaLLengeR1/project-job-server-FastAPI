from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.rental.billing.update import (
    update_billing_period_psql,
    update_billing_period_status_psql,
    update_meter_reading_psql,
)
from tests.core.repository.psql.rental.helper import make_billing_period, make_meter_reading


class TestUpdateBillingPeriodPsql:
    def test_update01_updates_rates_and_bill(self, db_session: Session):
        period = make_billing_period(db_session, electricity_bill_amount=None, electricity_rate=None)

        result, err, ok = update_billing_period_psql(
            str(period.id), 899.48, 1.05, True, 9.00, "korekta stawki", db_session=db_session
        )

        assert ok is True and err is None
        assert result.electricity_bill_amount == 899.48
        assert result.electricity_rate == 1.05
        assert result.electricity_rate_is_manual is True
        assert result.note == "korekta stawki"

    def test_update02_not_found(self, db_session: Session):
        result, err, ok = update_billing_period_psql(str(uuid4()), None, None, False, 9.00, None, db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestUpdateBillingPeriodStatusPsql:
    def test_update01_close_period(self, db_session: Session):
        period = make_billing_period(db_session, status="draft")

        result, err, ok = update_billing_period_status_psql(str(period.id), "closed", db_session=db_session)

        assert ok is True
        assert result.status == "closed"

    def test_update02_reopen_period(self, db_session: Session):
        period = make_billing_period(db_session, status="closed")

        result, err, ok = update_billing_period_status_psql(str(period.id), "draft", db_session=db_session)

        assert ok is True
        assert result.status == "draft"

    def test_update03_not_found(self, db_session: Session):
        result, err, ok = update_billing_period_status_psql(str(uuid4()), "closed", db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestUpdateMeterReadingPsql:
    def test_update01_updates_values_and_error_correction(self, db_session: Session):
        reading = make_meter_reading(db_session, previous_value=5621.26, current_value=5900.00, error_correction=0)

        # korekta odczytu "Teraz" + rozdzielony błąd licznika głównego (+1 kWh)
        result, err, ok = update_meter_reading_psql(str(reading.id), 5621.26, 5938.86, 1, db_session=db_session)

        assert ok is True and err is None
        assert result.current_value == 5938.86
        assert result.error_correction == 1

    def test_update02_not_found(self, db_session: Session):
        result, err, ok = update_meter_reading_psql(str(uuid4()), 0, 0, 0, db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"
