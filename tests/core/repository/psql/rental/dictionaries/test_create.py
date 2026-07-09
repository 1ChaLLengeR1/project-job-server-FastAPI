from datetime import date

from sqlalchemy.orm import Session

from core.repository.psql.rental.dictionaries.create import (
    create_apartment_cost_psql,
    create_apartment_psql,
    create_cost_type_psql,
    create_meter_psql,
    create_tenancy_psql,
    create_tenant_psql,
)
from tests.core.repository.psql.rental.helper import make_apartment, make_cost_type, make_tenant


class TestCreateApartmentPsql:
    def test_create01_returns_ok_with_fields(self, db_session: Session):
        result, err, ok = create_apartment_psql("Pokój Państwa Dudzik", "parter", db_session=db_session)

        assert ok is True and err is None
        assert result.id is not None
        assert result.name == "Pokój Państwa Dudzik"
        assert result.description == "parter"
        assert result.is_active is True
        assert result.created_at is not None

    def test_create02_duplicate_name_integrity_error(self, db_session: Session):
        make_apartment(db_session, name="Mieszkanie 4")

        result, err, ok = create_apartment_psql("Mieszkanie 4", db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "IntegrityError"


class TestCreateTenantPsql:
    def test_create01_returns_ok_with_fields(self, db_session: Session):
        result, err, ok = create_tenant_psql("Łukasz", "Kydr", note="tel. 600 000 000", db_session=db_session)

        assert ok is True and err is None
        assert result.first_name == "Łukasz"
        assert result.last_name == "Kydr"
        assert result.note == "tel. 600 000 000"
        assert result.is_active is True

    def test_create02_last_name_optional(self, db_session: Session):
        result, err, ok = create_tenant_psql("Witek", db_session=db_session)

        assert ok is True
        assert result.last_name is None


class TestCreateTenancyPsql:
    def test_create01_returns_ok_with_fields(self, db_session: Session):
        apartment = make_apartment(db_session)
        tenant = make_tenant(db_session)

        result, err, ok = create_tenancy_psql(
            str(apartment.id), str(tenant.id), 1100.00, 2, date(2026, 1, 1), db_session=db_session
        )

        assert ok is True and err is None
        assert result.apartment_id == str(apartment.id)
        assert result.tenant_id == str(tenant.id)
        assert result.rent_amount == 1100.00
        assert result.persons_count == 2
        assert result.start_date == date(2026, 1, 1)
        assert result.end_date is None

    def test_create02_unknown_apartment_integrity_error(self, db_session: Session):
        tenant = make_tenant(db_session)

        result, err, ok = create_tenancy_psql(
            "00000000-0000-0000-0000-000000000000",
            str(tenant.id),
            1000.00,
            1,
            date(2026, 1, 1),
            db_session=db_session,
        )

        assert ok is False
        assert err.key_type_error == "IntegrityError"


class TestCreateCostTypePsql:
    def test_create01_per_person(self, db_session: Session):
        result, err, ok = create_cost_type_psql("śmieci", "per_person", db_session=db_session)

        assert ok is True and err is None
        assert result.name == "śmieci"
        assert result.charge_type == "per_person"

    def test_create02_duplicate_name_integrity_error(self, db_session: Session):
        make_cost_type(db_session, name="garaż")

        result, err, ok = create_cost_type_psql("garaż", "fixed", db_session=db_session)

        assert ok is False
        assert err.key_type_error == "IntegrityError"


class TestCreateApartmentCostPsql:
    def test_create01_returns_ok_with_fields(self, db_session: Session):
        apartment = make_apartment(db_session)
        cost_type = make_cost_type(db_session, name="śmieci", charge_type="per_person")

        result, err, ok = create_apartment_cost_psql(
            str(apartment.id), str(cost_type.id), 35.00, date(2026, 1, 1), db_session=db_session
        )

        assert ok is True and err is None
        assert result.apartment_id == str(apartment.id)
        assert result.cost_type_id == str(cost_type.id)
        assert result.amount == 35.00
        assert result.end_date is None


class TestCreateMeterPsql:
    def test_create01_apartment_meter(self, db_session: Session):
        apartment = make_apartment(db_session)

        result, err, ok = create_meter_psql(
            "water", apartment_id=str(apartment.id), is_master=True, db_session=db_session
        )

        assert ok is True and err is None
        assert result.apartment_id == str(apartment.id)
        assert result.media_type == "water"
        assert result.is_master is True

    def test_create02_main_meter_without_apartment(self, db_session: Session):
        result, err, ok = create_meter_psql("electricity", db_session=db_session)

        assert ok is True
        assert result.apartment_id is None
        assert result.is_master is False
