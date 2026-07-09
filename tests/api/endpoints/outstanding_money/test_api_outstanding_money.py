from sqlalchemy.orm import Session

from api.endpoints.outstanding_money.collection import router as collection_router
from api.endpoints.outstanding_money.create import router as create_router
from api.endpoints.outstanding_money.delete import router as delete_router
from api.endpoints.outstanding_money.update import router as update_router
from database.psql.models.outstanding_money import NamesOverdue
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.outstanding_money.helper import make_item, make_overdue_list

MISSING_UUID = "6fa459ea-ee8a-4ca4-894e-db77e160355e"


class TestApiSuperadminCreateOutstandingList:
    def test_create_list01_returns_201_with_items(self, db_session: Session):
        client = make_client(db_session, create_router)
        payload = {"name": "lista", "array_object": [{"amount": 100.5, "name": "f1"}, {"amount": 50, "name": "f2"}]}

        with authorized_as("superadmin") as headers:
            response = client.post("/outstanding_money/create_list", json=payload, headers=headers)

        assert response.status_code == 201
        body = response.json()
        assert len(body["data"]["new_outstanding_money"]) == 2
        assert db_session.query(NamesOverdue).count() == 1

    def test_create_list02_empty_name_returns_422(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/outstanding_money/create_list", json={"name": " ", "array_object": []}, headers=headers
            )

        assert response.status_code == 422

    def test_create_list03_role_admin_returns_403(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("admin") as headers:
            response = client.post(
                "/outstanding_money/create_list", json={"name": "x", "array_object": []}, headers=headers
            )

        assert response.status_code == 403


class TestApiSuperadminAddOutstandingItem:
    def test_add_item01_returns_201(self, db_session: Session):
        overdue = make_overdue_list(db_session)
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/outstanding_money/add_item",
                json={"id_name": str(overdue.id), "amount": 25, "name": "pozycja"},
                headers=headers,
            )

        assert response.status_code == 201
        assert response.json()["data"]["amount"] == 25

    def test_add_item02_missing_list_returns_404(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/outstanding_money/add_item",
                json={"id_name": MISSING_UUID, "amount": 25, "name": "x"},
                headers=headers,
            )

        assert response.status_code == 404


class TestApiUserCollectionOutstandingMoney:
    def test_collection01_returns_lists_with_full_price(self, db_session: Session):
        overdue = make_overdue_list(db_session, name="lista A")
        make_item(db_session, id_name=overdue.id, amount=100.5)
        make_item(db_session, id_name=overdue.id, amount=50)
        client = make_client(db_session, collection_router)

        with authorized_as("user") as headers:
            response = client.get("/outstanding_money/collection", headers=headers)

        assert response.status_code == 200
        assert response.json()["data"][0]["full_price"] == 150.5


class TestApiSuperadminEditOutstanding:
    def test_edit01_list_name_and_item(self, db_session: Session):
        overdue = make_overdue_list(db_session, name="stara")
        item = make_item(db_session, id_name=overdue.id, amount=10)
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            list_response = client.put(
                "/outstanding_money/edit_name_list", json={"id": str(overdue.id), "name": "nowa"}, headers=headers
            )
            item_response = client.put(
                "/outstanding_money/edit_item",
                json={"id": str(item.id), "amount": 99, "name": "poprawiona"},
                headers=headers,
            )

        assert list_response.status_code == 200 and list_response.json()["data"]["name"] == "nowa"
        assert item_response.status_code == 200 and item_response.json()["data"]["amount"] == 99

    def test_edit02_missing_item_returns_404(self, db_session: Session):
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.put(
                "/outstanding_money/edit_item",
                json={"id": MISSING_UUID, "amount": 1, "name": "x"},
                headers=headers,
            )

        assert response.status_code == 404


class TestApiSuperadminDeleteOutstanding:
    def test_delete01_list_with_items(self, db_session: Session):
        overdue = make_overdue_list(db_session)
        make_item(db_session, id_name=overdue.id)
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete(f"/outstanding_money/delete_list/{overdue.id}", headers=headers)

        assert response.status_code == 200
        assert len(response.json()["data"]["outstanding_money"]) == 1
        assert db_session.query(NamesOverdue).count() == 0

    def test_delete02_item_invalid_uuid_returns_400(self, db_session: Session):
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete("/outstanding_money/delete_item/nie-uuid", headers=headers)

        assert response.status_code == 400
