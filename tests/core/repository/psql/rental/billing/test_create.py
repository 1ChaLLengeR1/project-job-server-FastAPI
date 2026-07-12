from datetime import date

from sqlalchemy.orm import Session

from core.repository.psql.rental.billing.create import (
    create_billing_period_psql,
    create_meter_reading_psql,
    create_settlement_psql,
)
from core.repository.psql.rental.billing.response import SettlementItemInput
from tests.core.repository.psql.rental.helper import (
    make_apartment,
    make_billing_period,
    make_cost_type,
    make_meter,
    make_meter_reading,
    make_tenancy,
)


class TestCreateBillingPeriodPsql:
    def test_create01_returns_ok_with_fields(self, db_session: Session):
        result, err, ok = create_billing_period_psql(
            date(2026, 6, 1), electricity_bill_amount=899.48, db_session=db_session
        )

        assert ok is True and err is None
        assert result.period_month == date(2026, 6, 1)
        assert result.status == "draft"
        assert result.electricity_bill_amount == 899.48
        assert result.water_rate == 9.00
        assert result.electricity_rate_is_manual is False

    def test_create02_normalizes_to_first_day_of_month(self, db_session: Session):
        result, err, ok = create_billing_period_psql(date(2026, 7, 15), db_session=db_session)

        assert ok is True
        assert result.period_month == date(2026, 7, 1)

    def test_create03_duplicate_month_integrity_error(self, db_session: Session):
        make_billing_period(db_session, period_month=date(2026, 6, 1))

        result, err, ok = create_billing_period_psql(date(2026, 6, 20), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "IntegrityError"


class TestCreateMeterReadingPsql:
    def test_create01_returns_ok_with_fields(self, db_session: Session):
        period = make_billing_period(db_session)
        meter = make_meter(db_session)

        # odczyty Państwa Dudzik z Obliczenia_3: 5621,26 -> 5938,86, błąd +1
        result, err, ok = create_meter_reading_psql(
            str(period.id), str(meter.id), 5621.26, 5938.86, 1, db_session=db_session
        )

        assert ok is True and err is None
        assert result.previous_value == 5621.26
        assert result.current_value == 5938.86
        assert result.error_correction == 1

    def test_create02_duplicate_period_meter_integrity_error(self, db_session: Session):
        period = make_billing_period(db_session)
        meter = make_meter(db_session)
        make_meter_reading(db_session, period=period, meter=meter)

        result, err, ok = create_meter_reading_psql(str(period.id), str(meter.id), 1, 2, db_session=db_session)

        assert ok is False
        assert err.key_type_error == "IntegrityError"


class TestCreateSettlementPsql:
    def test_create01_creates_with_items(self, db_session: Session):
        period = make_billing_period(db_session)
        apartment = make_apartment(db_session)
        tenancy = make_tenancy(db_session, apartment=apartment, rent_amount=1300.00, persons_count=2)
        smieci = make_cost_type(db_session, name="śmieci", charge_type="per_person")

        # rozliczenie Państwa Dudzik z Obliczenia_3: 335 + 64 + 70 + 60 + 200 - 200 = 529
        result, err, ok = create_settlement_psql(
            period_id=str(period.id),
            apartment_id=str(apartment.id),
            tenancy_id=str(tenancy.id),
            rent_amount=1300.00,
            electricity_consumption=318.6,
            electricity_cost=335.00,
            water_consumption=7.125,
            water_cost=64.00,
            total_media_amount=529.00,
            total_amount=1829.00,
            items=[
                SettlementItemInput("śmieci (2 os. x 35 zł)", "fixed_cost", 70.00, str(smieci.id)),
                SettlementItemInput("internet", "fixed_cost", 60.00),
                SettlementItemInput("garaż", "fixed_cost", 200.00),
                SettlementItemInput("rabat garaż", "adjustment", -200.00),
            ],
            db_session=db_session,
        )

        assert ok is True and err is None
        assert result.electricity_cost == 335.00
        assert result.total_media_amount == 529.00
        assert result.total_amount == 1829.00
        assert len(result.items) == 4
        assert result.items[0].cost_type_id == str(smieci.id)
        assert result.items[3].amount == -200.00

    def test_create02_vacant_apartment_without_tenancy(self, db_session: Session):
        period = make_billing_period(db_session)
        apartment = make_apartment(db_session)

        # Mieszkanie_4 z Obliczenia.txt: pustostan, tylko śmieci 27 zł
        result, err, ok = create_settlement_psql(
            period_id=str(period.id),
            apartment_id=str(apartment.id),
            tenancy_id=None,
            rent_amount=0,
            electricity_consumption=0,
            electricity_cost=0,
            water_consumption=0.002,
            water_cost=0,
            total_media_amount=27.00,
            total_amount=27.00,
            items=[SettlementItemInput("śmieci", "fixed_cost", 27.00)],
            db_session=db_session,
        )

        assert ok is True
        assert result.tenancy_id is None
        assert result.total_amount == 27.00

    def test_create03_duplicate_period_apartment_integrity_error(self, db_session: Session):
        period = make_billing_period(db_session)
        apartment = make_apartment(db_session)

        for _ in range(1):
            result, err, ok = create_settlement_psql(
                period_id=str(period.id),
                apartment_id=str(apartment.id),
                tenancy_id=None,
                rent_amount=0,
                electricity_consumption=0,
                electricity_cost=0,
                water_consumption=0,
                water_cost=0,
                total_media_amount=0,
                total_amount=0,
                items=[],
                db_session=db_session,
            )
            assert ok is True

        result, err, ok = create_settlement_psql(
            period_id=str(period.id),
            apartment_id=str(apartment.id),
            tenancy_id=None,
            rent_amount=0,
            electricity_consumption=0,
            electricity_cost=0,
            water_consumption=0,
            water_cost=0,
            total_media_amount=0,
            total_amount=0,
            items=[],
            db_session=db_session,
        )

        assert ok is False
        assert err.key_type_error == "IntegrityError"
