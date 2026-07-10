from uuid import uuid4

from sqlalchemy.orm import Session

from api.endpoints.rental.dictionaries.collection import router as collection_router
from api.endpoints.rental.dictionaries.create import router as create_router
from api.endpoints.rental.dictionaries.delete import router as delete_router
from api.endpoints.rental.dictionaries.one import router as one_router
from api.endpoints.rental.dictionaries.update import router as update_router
from database.psql.models.logs import Logs
from database.psql.models.rentals import RentalApartment, RentalMeter, RentalTenancy
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.rental.helper import (
    make_apartment,
    make_apartment_cost,
    make_cost_type,
    make_meter,
    make_tenancy,
    make_tenant,
)
from tests.core.repository.psql.user.helper import create_test_user

ALL_ROUTERS = (create_router, collection_router, one_router, update_router, delete_router)


class TestApiRentalApartments:
    def test_apartment01_create_returns_201_and_saves_row(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post("/rentals/apartments/create", json={"name": "Pokój Państwa Dudzik"}, headers=headers)

        assert response.status_code == 201
        body = response.json()
        assert body["status"] == "SUCCESS"
        assert body["data"]["name"] == "Pokój Państwa Dudzik" and body["data"]["is_active"] is True
        assert db_session.query(RentalApartment).count() == 1

    def test_apartment02_create_duplicate_name_returns_409(self, db_session: Session):
        make_apartment(db_session, name="Pokój Łukasza")
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post("/rentals/apartments/create", json={"name": "Pokój Łukasza"}, headers=headers)

        assert response.status_code == 409

    def test_apartment03_create_empty_name_returns_422(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post("/rentals/apartments/create", json={"name": "   "}, headers=headers)

        assert response.status_code == 422

    def test_apartment04_collection_filters_by_is_active(self, db_session: Session):
        make_apartment(db_session, name="Aktywne")
        make_apartment(db_session, name="Nieaktywne", is_active=False)
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            all_rows = client.get("/rentals/apartments/collection", headers=headers)
            active_rows = client.get("/rentals/apartments/collection", params={"is_active": True}, headers=headers)

        assert len(all_rows.json()["data"]) == 2
        active_names = [row["name"] for row in active_rows.json()["data"]]
        assert active_names == ["Aktywne"]

    def test_apartment05_one_returns_apartment_and_404_for_missing(self, db_session: Session):
        apartment = make_apartment(db_session, name="Pokój Witka")
        client = make_client(db_session, one_router)

        with authorized_as("superadmin") as headers:
            found = client.get(f"/rentals/apartments/one/{apartment.id}", headers=headers)
            missing = client.get(f"/rentals/apartments/one/{uuid4()}", headers=headers)

        assert found.status_code == 200 and found.json()["data"]["name"] == "Pokój Witka"
        assert missing.status_code == 404

    def test_apartment06_one_invalid_uuid_returns_400(self, db_session: Session):
        client = make_client(db_session, one_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/rentals/apartments/one/not-a-uuid", headers=headers)

        assert response.status_code == 400

    def test_apartment07_update_returns_200_and_changes_row(self, db_session: Session):
        apartment = make_apartment(db_session, name="Stara nazwa")
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.put(
                f"/rentals/apartments/update/{apartment.id}",
                json={"name": "Nowa nazwa", "description": None, "is_active": False},
                headers=headers,
            )

        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Nowa nazwa"
        assert response.json()["data"]["is_active"] is False

    def test_apartment08_delete_returns_200_and_removes_row(self, db_session: Session):
        apartment = make_apartment(db_session)
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete(f"/rentals/apartments/delete/{apartment.id}", headers=headers)

        assert response.status_code == 200
        assert db_session.query(RentalApartment).count() == 0

    def test_apartment09_delete_with_relations_returns_409(self, db_session: Session):
        apartment = make_apartment(db_session)
        make_meter(db_session, apartment=apartment)
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete(f"/rentals/apartments/delete/{apartment.id}", headers=headers)

        assert response.status_code == 409

    def test_apartment10_no_token_401_and_role_user_403(self, db_session: Session):
        client = make_client(db_session, create_router)

        no_token = client.post("/rentals/apartments/create", json={"name": "x"})
        with authorized_as("user") as headers:
            wrong_role = client.post("/rentals/apartments/create", json={"name": "x"}, headers=headers)

        assert no_token.status_code == 401
        assert wrong_role.status_code == 403

    def test_apartment11_create_writes_audit_log(self, db_session: Session):
        user = create_test_user(db_session, type="superadmin")
        client = make_client(db_session, create_router)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            client.post("/rentals/apartments/create", json={"name": "Audytowane"}, headers=headers)

        log = db_session.query(Logs).filter(Logs.description == "rental:create_apartment").first()
        assert log is not None and log.username == user.username


class TestApiRentalTenants:
    def test_tenant01_create_returns_201(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/rentals/tenants/create",
                json={"first_name": "Łukasz", "last_name": "Kydr", "note": "tel. 500 600 700"},
                headers=headers,
            )

        assert response.status_code == 201
        assert response.json()["data"]["first_name"] == "Łukasz"

    def test_tenant02_collection_and_one(self, db_session: Session):
        tenant = make_tenant(db_session, first_name="Ania", last_name=None)
        client = make_client(db_session, collection_router, one_router)

        with authorized_as("superadmin") as headers:
            collection = client.get("/rentals/tenants/collection", headers=headers)
            one = client.get(f"/rentals/tenants/one/{tenant.id}", headers=headers)

        assert len(collection.json()["data"]) == 1
        assert one.json()["data"]["first_name"] == "Ania"

    def test_tenant03_update_returns_200(self, db_session: Session):
        tenant = make_tenant(db_session, first_name="Ania")
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.put(
                f"/rentals/tenants/update/{tenant.id}",
                json={"first_name": "Witek", "last_name": None, "note": None, "is_active": True},
                headers=headers,
            )

        assert response.status_code == 200
        assert response.json()["data"]["first_name"] == "Witek"

    def test_tenant04_delete_returns_200_and_404_for_missing(self, db_session: Session):
        tenant = make_tenant(db_session)
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            deleted = client.delete(f"/rentals/tenants/delete/{tenant.id}", headers=headers)
            missing = client.delete(f"/rentals/tenants/delete/{uuid4()}", headers=headers)

        assert deleted.status_code == 200
        assert missing.status_code == 404


class TestApiRentalTenancies:
    def test_tenancy01_create_returns_201_and_saves_row(self, db_session: Session):
        apartment = make_apartment(db_session)
        tenant = make_tenant(db_session)
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/rentals/tenancies/create",
                json={
                    "apartment_id": str(apartment.id),
                    "tenant_id": str(tenant.id),
                    "rent_amount": 1100.00,
                    "persons_count": 2,
                    "start_date": "2026-01-01",
                },
                headers=headers,
            )

        assert response.status_code == 201
        body = response.json()["data"]
        assert body["rent_amount"] == 1100.00 and body["persons_count"] == 2
        assert db_session.query(RentalTenancy).count() == 1

    def test_tenancy02_create_invalid_uuid_in_payload_returns_422(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/rentals/tenancies/create",
                json={
                    "apartment_id": "not-a-uuid",
                    "tenant_id": str(uuid4()),
                    "rent_amount": 1000,
                    "start_date": "2026-01-01",
                },
                headers=headers,
            )

        assert response.status_code == 422

    def test_tenancy03_collection_filters_by_apartment(self, db_session: Session):
        apartment = make_apartment(db_session)
        make_tenancy(db_session, apartment=apartment)
        make_tenancy(db_session)
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get(
                "/rentals/tenancies/collection", params={"apartment_id": str(apartment.id)}, headers=headers
            )

        rows = response.json()["data"]
        assert len(rows) == 1 and rows[0]["apartment_id"] == str(apartment.id)

    def test_tenancy04_one_update_delete(self, db_session: Session):
        tenancy = make_tenancy(db_session, rent_amount=1000.00)
        client = make_client(db_session, one_router, update_router, delete_router)

        with authorized_as("superadmin") as headers:
            one = client.get(f"/rentals/tenancies/one/{tenancy.id}", headers=headers)
            updated = client.put(
                f"/rentals/tenancies/update/{tenancy.id}",
                json={
                    "rent_amount": 1200.00,
                    "persons_count": 1,
                    "start_date": "2026-01-01",
                    "end_date": "2026-06-30",
                },
                headers=headers,
            )
            deleted = client.delete(f"/rentals/tenancies/delete/{tenancy.id}", headers=headers)

        assert one.status_code == 200
        assert updated.status_code == 200 and updated.json()["data"]["rent_amount"] == 1200.00
        assert deleted.status_code == 200


class TestApiRentalCostTypes:
    def test_cost_type01_create_returns_201(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/rentals/cost_types/create", json={"name": "śmieci", "charge_type": "per_person"}, headers=headers
            )

        assert response.status_code == 201
        assert response.json()["data"]["charge_type"] == "per_person"

    def test_cost_type02_create_invalid_charge_type_returns_422(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/rentals/cost_types/create", json={"name": "śmieci", "charge_type": "hourly"}, headers=headers
            )

        assert response.status_code == 422

    def test_cost_type03_collection_and_one(self, db_session: Session):
        cost_type = make_cost_type(db_session, name="garaż")
        client = make_client(db_session, collection_router, one_router)

        with authorized_as("superadmin") as headers:
            collection = client.get("/rentals/cost_types/collection", headers=headers)
            one = client.get(f"/rentals/cost_types/one/{cost_type.id}", headers=headers)

        assert len(collection.json()["data"]) == 1
        assert one.json()["data"]["name"] == "garaż"

    def test_cost_type04_update_and_delete(self, db_session: Session):
        cost_type = make_cost_type(db_session, name="internet")
        client = make_client(db_session, update_router, delete_router)

        with authorized_as("superadmin") as headers:
            updated = client.put(
                f"/rentals/cost_types/update/{cost_type.id}",
                json={"name": "internet światłowód", "charge_type": "fixed", "is_active": True},
                headers=headers,
            )
            deleted = client.delete(f"/rentals/cost_types/delete/{cost_type.id}", headers=headers)

        assert updated.status_code == 200 and updated.json()["data"]["name"] == "internet światłowód"
        assert deleted.status_code == 200


class TestApiRentalApartmentCosts:
    def test_apartment_cost01_create_returns_201(self, db_session: Session):
        apartment = make_apartment(db_session)
        cost_type = make_cost_type(db_session, name="internet")
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/rentals/apartment_costs/create",
                json={
                    "apartment_id": str(apartment.id),
                    "cost_type_id": str(cost_type.id),
                    "amount": 60.00,
                    "start_date": "2026-01-01",
                },
                headers=headers,
            )

        assert response.status_code == 201
        assert response.json()["data"]["amount"] == 60.00

    def test_apartment_cost02_collection_filters_by_apartment(self, db_session: Session):
        apartment = make_apartment(db_session)
        make_apartment_cost(db_session, apartment=apartment)
        make_apartment_cost(db_session)
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get(
                "/rentals/apartment_costs/collection", params={"apartment_id": str(apartment.id)}, headers=headers
            )

        rows = response.json()["data"]
        assert len(rows) == 1 and rows[0]["apartment_id"] == str(apartment.id)

    def test_apartment_cost03_one_update_delete(self, db_session: Session):
        apartment_cost = make_apartment_cost(db_session, amount=30.00)
        client = make_client(db_session, one_router, update_router, delete_router)

        with authorized_as("superadmin") as headers:
            one = client.get(f"/rentals/apartment_costs/one/{apartment_cost.id}", headers=headers)
            updated = client.put(
                f"/rentals/apartment_costs/update/{apartment_cost.id}",
                json={"amount": 60.00, "start_date": "2026-01-01", "end_date": None},
                headers=headers,
            )
            deleted = client.delete(f"/rentals/apartment_costs/delete/{apartment_cost.id}", headers=headers)

        assert one.status_code == 200
        assert updated.status_code == 200 and updated.json()["data"]["amount"] == 60.00
        assert deleted.status_code == 200


class TestApiRentalMeters:
    def test_meter01_create_main_meter_without_apartment(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/rentals/meters/create",
                json={"media_type": "electricity", "name": "licznik główny budynku"},
                headers=headers,
            )

        assert response.status_code == 201
        body = response.json()["data"]
        assert body["apartment_id"] is None and body["is_master"] is False
        assert db_session.query(RentalMeter).count() == 1

    def test_meter02_create_master_water_meter_for_apartment(self, db_session: Session):
        apartment = make_apartment(db_session)
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/rentals/meters/create",
                json={"media_type": "water", "apartment_id": str(apartment.id), "is_master": True},
                headers=headers,
            )

        assert response.status_code == 201
        assert response.json()["data"]["is_master"] is True

    def test_meter03_create_invalid_media_type_returns_422(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post("/rentals/meters/create", json={"media_type": "gas"}, headers=headers)

        assert response.status_code == 422

    def test_meter04_collection_filters_by_media_type(self, db_session: Session):
        make_meter(db_session, media_type="electricity")
        make_meter(db_session, media_type="water")
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/rentals/meters/collection", params={"media_type": "water"}, headers=headers)

        rows = response.json()["data"]
        assert len(rows) == 1 and rows[0]["media_type"] == "water"

    def test_meter05_one_update_delete(self, db_session: Session):
        meter = make_meter(db_session)
        client = make_client(db_session, one_router, update_router, delete_router)

        with authorized_as("superadmin") as headers:
            one = client.get(f"/rentals/meters/one/{meter.id}", headers=headers)
            updated = client.put(
                f"/rentals/meters/update/{meter.id}",
                json={"is_master": True, "name": "licznik nadrzędny", "is_active": True},
                headers=headers,
            )
            deleted = client.delete(f"/rentals/meters/delete/{meter.id}", headers=headers)

        assert one.status_code == 200
        assert updated.status_code == 200 and updated.json()["data"]["is_master"] is True
        assert deleted.status_code == 200
