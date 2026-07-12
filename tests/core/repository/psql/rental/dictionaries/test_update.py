from datetime import date
from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.rental.dictionaries.update import (
    update_apartment_cost_psql,
    update_apartment_psql,
    update_cost_type_psql,
    update_meter_psql,
    update_tenancy_psql,
    update_tenant_psql,
)
from tests.core.repository.psql.rental.helper import (
    make_apartment,
    make_apartment_cost,
    make_cost_type,
    make_meter,
    make_tenancy,
    make_tenant,
)


class TestUpdateApartmentPsql:
    def test_update01_updates_fields(self, db_session: Session):
        apartment = make_apartment(db_session, name="Pokój Anii")

        result, err, ok = update_apartment_psql(
            str(apartment.id), "Pokój Witka", "zmiana najemcy", False, db_session=db_session
        )

        assert ok is True and err is None
        assert result.name == "Pokój Witka"
        assert result.description == "zmiana najemcy"
        assert result.is_active is False

    def test_update02_not_found(self, db_session: Session):
        result, err, ok = update_apartment_psql(str(uuid4()), "X", None, True, db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"

    def test_update03_duplicate_name_integrity_error(self, db_session: Session):
        make_apartment(db_session, name="Mieszkanie 4")
        apartment = make_apartment(db_session, name="Pokój Łukasza")

        result, err, ok = update_apartment_psql(str(apartment.id), "Mieszkanie 4", None, True, db_session=db_session)

        assert ok is False
        assert err.key_type_error == "IntegrityError"


class TestUpdateTenantPsql:
    def test_update01_updates_fields(self, db_session: Session):
        tenant = make_tenant(db_session, first_name="Krzysiek", last_name="Krupa")

        result, err, ok = update_tenant_psql(
            str(tenant.id), "Krzysztof", "Krupa", "wyprowadził się", False, db_session=db_session
        )

        assert ok is True
        assert result.first_name == "Krzysztof"
        assert result.note == "wyprowadził się"
        assert result.is_active is False

    def test_update02_not_found(self, db_session: Session):
        result, err, ok = update_tenant_psql(str(uuid4()), "X", None, None, True, db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestUpdateTenancyPsql:
    def test_update01_close_tenancy_sets_end_date(self, db_session: Session):
        tenancy = make_tenancy(db_session, rent_amount=1000.00, start_date=date(2025, 1, 1))

        result, err, ok = update_tenancy_psql(
            str(tenancy.id), 1000.00, 1, date(2025, 1, 1), date(2026, 5, 31), db_session=db_session
        )

        assert ok is True
        assert result.end_date == date(2026, 5, 31)

    def test_update02_rent_and_persons_change(self, db_session: Session):
        tenancy = make_tenancy(db_session, rent_amount=1000.00, persons_count=1)

        result, err, ok = update_tenancy_psql(
            str(tenancy.id), 1300.00, 2, date(2026, 1, 1), None, db_session=db_session
        )

        assert ok is True
        assert result.rent_amount == 1300.00
        assert result.persons_count == 2

    def test_update03_not_found(self, db_session: Session):
        result, err, ok = update_tenancy_psql(str(uuid4()), 1000.00, 1, date(2026, 1, 1), None, db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestUpdateCostTypePsql:
    def test_update01_updates_fields(self, db_session: Session):
        cost_type = make_cost_type(db_session, name="śmieci stare", charge_type="fixed")

        result, err, ok = update_cost_type_psql(str(cost_type.id), "śmieci", "per_person", True, db_session=db_session)

        assert ok is True
        assert result.name == "śmieci"
        assert result.charge_type == "per_person"

    def test_update02_not_found(self, db_session: Session):
        result, err, ok = update_cost_type_psql(str(uuid4()), "x", "fixed", True, db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestUpdateApartmentCostPsql:
    def test_update01_updates_amount_and_dates(self, db_session: Session):
        apartment_cost = make_apartment_cost(db_session, amount=30.00, start_date=date(2025, 1, 1))

        result, err, ok = update_apartment_cost_psql(
            str(apartment_cost.id), 60.00, date(2025, 1, 1), date(2026, 5, 31), db_session=db_session
        )

        assert ok is True
        assert result.amount == 60.00
        assert result.end_date == date(2026, 5, 31)

    def test_update02_not_found(self, db_session: Session):
        result, err, ok = update_apartment_cost_psql(str(uuid4()), 60.00, date(2026, 1, 1), None, db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestUpdateMeterPsql:
    def test_update01_updates_fields(self, db_session: Session):
        meter = make_meter(db_session, media_type="water", is_master=False)

        result, err, ok = update_meter_psql(
            str(meter.id), True, "licznik nadrzędny Łukasza", True, db_session=db_session
        )

        assert ok is True
        assert result.is_master is True
        assert result.name == "licznik nadrzędny Łukasza"

    def test_update02_not_found(self, db_session: Session):
        result, err, ok = update_meter_psql(str(uuid4()), False, None, True, db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"
