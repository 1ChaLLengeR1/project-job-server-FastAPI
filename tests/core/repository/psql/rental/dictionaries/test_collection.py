from datetime import date

from sqlalchemy.orm import Session

from core.repository.psql.rental.dictionaries.collection import (
    collection_apartment_costs_psql,
    collection_apartments_psql,
    collection_cost_types_psql,
    collection_meters_psql,
    collection_tenancies_psql,
    collection_tenants_psql,
)
from tests.core.repository.psql.rental.helper import (
    make_apartment,
    make_apartment_cost,
    make_cost_type,
    make_meter,
    make_tenancy,
    make_tenant,
)


class TestCollectionApartmentsPsql:
    def test_collection01_returns_all_sorted_by_name(self, db_session: Session):
        make_apartment(db_session, name="Pokój Łukasza")
        make_apartment(db_session, name="Mieszkanie 4")

        result, err, ok = collection_apartments_psql(db_session=db_session)

        assert ok is True and err is None
        assert [apartment.name for apartment in result] == ["Mieszkanie 4", "Pokój Łukasza"]

    def test_collection02_filter_is_active(self, db_session: Session):
        make_apartment(db_session, name="Aktywne")
        make_apartment(db_session, name="Nieaktywne", is_active=False)

        result, err, ok = collection_apartments_psql(is_active=True, db_session=db_session)

        assert ok is True
        assert [apartment.name for apartment in result] == ["Aktywne"]

    def test_collection03_empty(self, db_session: Session):
        result, err, ok = collection_apartments_psql(db_session=db_session)

        assert ok is True
        assert result == []


class TestCollectionTenantsPsql:
    def test_collection01_filter_is_active(self, db_session: Session):
        make_tenant(db_session, first_name="Ania", last_name=None)
        make_tenant(db_session, first_name="Witek", last_name=None, is_active=False)

        result, err, ok = collection_tenants_psql(is_active=False, db_session=db_session)

        assert ok is True
        assert [tenant.first_name for tenant in result] == ["Witek"]


class TestCollectionTenanciesPsql:
    def test_collection01_filter_by_apartment(self, db_session: Session):
        apartment = make_apartment(db_session)
        make_tenancy(db_session, apartment=apartment, rent_amount=1100.00)
        make_tenancy(db_session, rent_amount=1000.00)  # inne mieszkanie

        result, err, ok = collection_tenancies_psql(apartment_id=str(apartment.id), db_session=db_session)

        assert ok is True
        assert len(result) == 1
        assert result[0].rent_amount == 1100.00

    def test_collection02_active_on_excludes_ended(self, db_session: Session):
        apartment = make_apartment(db_session)
        # Ania wyprowadziła się w maju, Witek od czerwca (Obliczenia_2 -> Obliczenia_3)
        make_tenancy(
            db_session,
            apartment=apartment,
            tenant=make_tenant(db_session, first_name="Ania", last_name=None),
            start_date=date(2025, 1, 1),
            end_date=date(2026, 5, 31),
        )
        witek = make_tenant(db_session, first_name="Witek", last_name=None)
        make_tenancy(db_session, apartment=apartment, tenant=witek, start_date=date(2026, 6, 1))

        result, err, ok = collection_tenancies_psql(
            apartment_id=str(apartment.id), active_on=date(2026, 6, 15), db_session=db_session
        )

        assert ok is True
        assert len(result) == 1
        assert result[0].tenant_id == str(witek.id)

    def test_collection03_filter_by_tenant(self, db_session: Session):
        tenant = make_tenant(db_session)
        make_tenancy(db_session, tenant=tenant)
        make_tenancy(db_session)

        result, err, ok = collection_tenancies_psql(tenant_id=str(tenant.id), db_session=db_session)

        assert ok is True
        assert len(result) == 1


class TestCollectionCostTypesPsql:
    def test_collection01_sorted_by_name(self, db_session: Session):
        make_cost_type(db_session, name="śmieci", charge_type="per_person")
        make_cost_type(db_session, name="internet")
        make_cost_type(db_session, name="garaż")

        result, err, ok = collection_cost_types_psql(db_session=db_session)

        assert ok is True
        assert [cost_type.name for cost_type in result] == ["garaż", "internet", "śmieci"]


class TestCollectionApartmentCostsPsql:
    def test_collection01_filter_by_apartment(self, db_session: Session):
        apartment = make_apartment(db_session)
        make_apartment_cost(db_session, apartment=apartment, amount=60.00)
        make_apartment_cost(db_session, amount=30.00)  # inne mieszkanie

        result, err, ok = collection_apartment_costs_psql(apartment_id=str(apartment.id), db_session=db_session)

        assert ok is True
        assert len(result) == 1
        assert result[0].amount == 60.00

    def test_collection02_active_on_respects_rate_history(self, db_session: Session):
        # internet Anii: 30 zł do maja, 60 zł od czerwca (zmiana stawki = nowy rekord)
        apartment = make_apartment(db_session)
        cost_type = make_cost_type(db_session, name="internet")
        make_apartment_cost(
            db_session,
            apartment=apartment,
            cost_type=cost_type,
            amount=30.00,
            start_date=date(2025, 1, 1),
            end_date=date(2026, 5, 31),
        )
        make_apartment_cost(
            db_session, apartment=apartment, cost_type=cost_type, amount=60.00, start_date=date(2026, 6, 1)
        )

        result, err, ok = collection_apartment_costs_psql(
            apartment_id=str(apartment.id), active_on=date(2026, 6, 1), db_session=db_session
        )

        assert ok is True
        assert len(result) == 1
        assert result[0].amount == 60.00


class TestCollectionMetersPsql:
    def test_collection01_filter_media_type(self, db_session: Session):
        apartment = make_apartment(db_session)
        make_meter(db_session, apartment=apartment, media_type="electricity")
        make_meter(db_session, apartment=apartment, media_type="water")

        result, err, ok = collection_meters_psql(media_type="water", db_session=db_session)

        assert ok is True
        assert len(result) == 1
        assert result[0].media_type == "water"

    def test_collection02_filter_by_apartment_and_active(self, db_session: Session):
        apartment = make_apartment(db_session)
        make_meter(db_session, apartment=apartment)
        make_meter(db_session, apartment=apartment, is_active=False)
        make_meter(db_session)  # licznik główny (bez mieszkania)

        result, err, ok = collection_meters_psql(apartment_id=str(apartment.id), is_active=True, db_session=db_session)

        assert ok is True
        assert len(result) == 1
