from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.rental.dictionaries.one import (
    one_apartment_cost_psql,
    one_apartment_psql,
    one_cost_type_psql,
    one_meter_psql,
    one_tenancy_psql,
    one_tenant_psql,
)
from tests.core.repository.psql.rental.helper import (
    make_apartment,
    make_apartment_cost,
    make_cost_type,
    make_meter,
    make_tenancy,
    make_tenant,
)


class TestOneApartmentPsql:
    def test_one01_returns_apartment(self, db_session: Session):
        apartment = make_apartment(db_session, name="Pokój Łukasza")

        result, err, ok = one_apartment_psql(str(apartment.id), db_session=db_session)

        assert ok is True and err is None
        assert result.id == str(apartment.id)
        assert result.name == "Pokój Łukasza"

    def test_one02_not_found(self, db_session: Session):
        result, err, ok = one_apartment_psql(str(uuid4()), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"


class TestOneTenantPsql:
    def test_one01_returns_tenant(self, db_session: Session):
        tenant = make_tenant(db_session, first_name="Ania", last_name=None)

        result, err, ok = one_tenant_psql(str(tenant.id), db_session=db_session)

        assert ok is True
        assert result.first_name == "Ania"

    def test_one02_not_found(self, db_session: Session):
        result, err, ok = one_tenant_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestOneTenancyPsql:
    def test_one01_returns_tenancy(self, db_session: Session):
        tenancy = make_tenancy(db_session, rent_amount=1200.00)

        result, err, ok = one_tenancy_psql(str(tenancy.id), db_session=db_session)

        assert ok is True
        assert result.rent_amount == 1200.00

    def test_one02_not_found(self, db_session: Session):
        result, err, ok = one_tenancy_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestOneCostTypePsql:
    def test_one01_returns_cost_type(self, db_session: Session):
        cost_type = make_cost_type(db_session, name="przesył")

        result, err, ok = one_cost_type_psql(str(cost_type.id), db_session=db_session)

        assert ok is True
        assert result.name == "przesył"

    def test_one02_not_found(self, db_session: Session):
        result, err, ok = one_cost_type_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestOneApartmentCostPsql:
    def test_one01_returns_apartment_cost(self, db_session: Session):
        apartment_cost = make_apartment_cost(db_session, amount=200.00)

        result, err, ok = one_apartment_cost_psql(str(apartment_cost.id), db_session=db_session)

        assert ok is True
        assert result.amount == 200.00

    def test_one02_not_found(self, db_session: Session):
        result, err, ok = one_apartment_cost_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestOneMeterPsql:
    def test_one01_returns_meter(self, db_session: Session):
        meter = make_meter(db_session, media_type="water", is_master=True)

        result, err, ok = one_meter_psql(str(meter.id), db_session=db_session)

        assert ok is True
        assert result.media_type == "water"
        assert result.is_master is True

    def test_one02_not_found(self, db_session: Session):
        result, err, ok = one_meter_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"
