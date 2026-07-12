from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.rental.billing.delete import (
    delete_billing_period_psql,
    delete_meter_reading_psql,
    delete_settlements_by_period_psql,
)
from database.psql.models.rentals import (
    RentalBeneficiarySettlement,
    RentalBeneficiarySettlementItem,
    RentalBillingPeriod,
    RentalMeterReading,
    RentalSettlement,
    RentalSettlementItem,
)
from tests.core.repository.psql.rental.helper import (
    make_beneficiary_settlement,
    make_beneficiary_settlement_item,
    make_billing_period,
    make_meter_reading,
    make_settlement,
    make_settlement_item,
)


def _make_full_period(db_session: Session):
    """Okres z odczytem, rozliczeniem mieszkania (+item) i podziałem rodzinnym (+item)."""
    period = make_billing_period(db_session)
    make_meter_reading(db_session, period=period)
    settlement = make_settlement(db_session, period=period)
    make_settlement_item(db_session, settlement=settlement)
    beneficiary_settlement = make_beneficiary_settlement(db_session, period=period)
    make_beneficiary_settlement_item(db_session, beneficiary_settlement=beneficiary_settlement)
    return period


class TestDeleteBillingPeriodPsql:
    def test_delete01_cascades_readings_and_snapshots(self, db_session: Session):
        period = _make_full_period(db_session)

        result, err, ok = delete_billing_period_psql(str(period.id), db_session=db_session)

        assert ok is True and err is None
        assert db_session.query(RentalBillingPeriod).count() == 0
        assert db_session.query(RentalMeterReading).count() == 0
        assert db_session.query(RentalSettlement).count() == 0
        assert db_session.query(RentalSettlementItem).count() == 0
        assert db_session.query(RentalBeneficiarySettlement).count() == 0
        assert db_session.query(RentalBeneficiarySettlementItem).count() == 0

    def test_delete02_not_found(self, db_session: Session):
        result, err, ok = delete_billing_period_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestDeleteMeterReadingPsql:
    def test_delete01_deletes(self, db_session: Session):
        reading = make_meter_reading(db_session)

        result, err, ok = delete_meter_reading_psql(str(reading.id), db_session=db_session)

        assert ok is True
        assert db_session.query(RentalMeterReading).count() == 0

    def test_delete02_not_found(self, db_session: Session):
        result, err, ok = delete_meter_reading_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestDeleteSettlementsByPeriodPsql:
    def test_delete01_reopen_removes_snapshots_keeps_readings(self, db_session: Session):
        period = _make_full_period(db_session)

        result, err, ok = delete_settlements_by_period_psql(str(period.id), db_session=db_session)

        assert ok is True and err is None
        assert result == 1  # liczba usuniętych rozliczeń mieszkań
        assert db_session.query(RentalSettlement).count() == 0
        assert db_session.query(RentalSettlementItem).count() == 0
        assert db_session.query(RentalBeneficiarySettlement).count() == 0
        assert db_session.query(RentalBeneficiarySettlementItem).count() == 0
        # odczyty i sam okres zostają — reopen nie kasuje danych wejściowych
        assert db_session.query(RentalMeterReading).count() == 1
        assert db_session.query(RentalBillingPeriod).count() == 1

    def test_delete02_not_found(self, db_session: Session):
        result, err, ok = delete_settlements_by_period_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"
