from uuid import uuid4

from sqlalchemy.orm import Session

from core.repository.psql.rental.dictionaries.delete import (
    delete_apartment_cost_psql,
    delete_apartment_psql,
    delete_cost_type_psql,
    delete_meter_psql,
    delete_tenancy_psql,
    delete_tenant_psql,
)
from tests.core.repository.psql.rental.helper import (
    make_apartment,
    make_apartment_cost,
    make_cost_type,
    make_meter,
    make_tenancy,
    make_tenant,
)


class TestDeleteApartmentPsql:
    def test_delete01_deletes_and_returns_snapshot(self, db_session: Session):
        apartment = make_apartment(db_session, name="Mieszkanie 4")

        result, err, ok = delete_apartment_psql(str(apartment.id), db_session=db_session)

        assert ok is True and err is None
        assert result.name == "Mieszkanie 4"

    def test_delete02_not_found(self, db_session: Session):
        result, err, ok = delete_apartment_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"

    def test_delete03_restrict_blocks_with_tenancy(self, db_session: Session):
        apartment = make_apartment(db_session)
        make_tenancy(db_session, apartment=apartment)

        result, err, ok = delete_apartment_psql(str(apartment.id), db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "IntegrityError"

    def test_delete04_restrict_blocks_with_meter(self, db_session: Session):
        apartment = make_apartment(db_session)
        make_meter(db_session, apartment=apartment)

        result, err, ok = delete_apartment_psql(str(apartment.id), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "IntegrityError"


class TestDeleteTenantPsql:
    def test_delete01_deletes(self, db_session: Session):
        tenant = make_tenant(db_session)

        result, err, ok = delete_tenant_psql(str(tenant.id), db_session=db_session)

        assert ok is True

    def test_delete02_restrict_blocks_with_tenancy(self, db_session: Session):
        tenant = make_tenant(db_session)
        make_tenancy(db_session, tenant=tenant)

        result, err, ok = delete_tenant_psql(str(tenant.id), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "IntegrityError"

    def test_delete03_not_found(self, db_session: Session):
        result, err, ok = delete_tenant_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestDeleteTenancyPsql:
    def test_delete01_deletes(self, db_session: Session):
        tenancy = make_tenancy(db_session)

        result, err, ok = delete_tenancy_psql(str(tenancy.id), db_session=db_session)

        assert ok is True

    def test_delete02_not_found(self, db_session: Session):
        result, err, ok = delete_tenancy_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestDeleteCostTypePsql:
    def test_delete01_deletes(self, db_session: Session):
        cost_type = make_cost_type(db_session)

        result, err, ok = delete_cost_type_psql(str(cost_type.id), db_session=db_session)

        assert ok is True

    def test_delete02_restrict_blocks_with_apartment_cost(self, db_session: Session):
        cost_type = make_cost_type(db_session)
        make_apartment_cost(db_session, cost_type=cost_type)

        result, err, ok = delete_cost_type_psql(str(cost_type.id), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "IntegrityError"

    def test_delete03_not_found(self, db_session: Session):
        result, err, ok = delete_cost_type_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestDeleteApartmentCostPsql:
    def test_delete01_deletes(self, db_session: Session):
        apartment_cost = make_apartment_cost(db_session)

        result, err, ok = delete_apartment_cost_psql(str(apartment_cost.id), db_session=db_session)

        assert ok is True

    def test_delete02_not_found(self, db_session: Session):
        result, err, ok = delete_apartment_cost_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"


class TestDeleteMeterPsql:
    def test_delete01_deletes(self, db_session: Session):
        meter = make_meter(db_session)

        result, err, ok = delete_meter_psql(str(meter.id), db_session=db_session)

        assert ok is True

    def test_delete02_not_found(self, db_session: Session):
        result, err, ok = delete_meter_psql(str(uuid4()), db_session=db_session)

        assert ok is False
        assert err.key_type_error == "NotFound"
