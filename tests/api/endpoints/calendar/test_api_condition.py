from sqlalchemy.orm import Session

from api.endpoints.calendar.condition.collection import router as collection_router
from api.endpoints.calendar.condition.create import router as create_router
from api.endpoints.calendar.condition.delete import router as delete_router
from api.endpoints.calendar.condition.update import router as update_router
from database.psql.models.calendar import WorkConditionChange
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.calendar.helper import make_condition

MISSING_UUID = "6fa459ea-ee8a-4ca4-894e-db77e160355e"


class TestApiSuperadminCreateWorkCondition:
    def test_create01_returns_201(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/calendar/condition/create", json={"norm_hours": 8, "hourly_rate": 30.5}, headers=headers
            )

        assert response.status_code == 201
        assert response.json()["data"]["hourly_rate"] == 30.5

    def test_create02_zero_norm_hours_returns_422(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/calendar/condition/create", json={"norm_hours": 0, "hourly_rate": 30}, headers=headers
            )

        assert response.status_code == 422


class TestApiUserCollectionWorkConditions:
    def test_collection01_returns_conditions(self, db_session: Session):
        make_condition(db_session, norm_hours=8)
        client = make_client(db_session, collection_router)

        with authorized_as("user") as headers:
            response = client.get("/calendar/condition/collection", headers=headers)

        assert response.status_code == 200
        assert len(response.json()["data"]) == 1


class TestApiSuperadminUpdateWorkCondition:
    def test_update01_changes_values(self, db_session: Session):
        condition = make_condition(db_session, norm_hours=8)
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.patch(
                f"/calendar/condition/update/{condition.id}",
                json={"norm_hours": 7.5, "hourly_rate": 35},
                headers=headers,
            )

        assert response.status_code == 200
        assert response.json()["data"]["norm_hours"] == 7.5

    def test_update02_missing_returns_404_invalid_uuid_400(self, db_session: Session):
        client = make_client(db_session, update_router)
        payload = {"norm_hours": 8, "hourly_rate": 30}

        with authorized_as("superadmin") as headers:
            missing = client.patch(f"/calendar/condition/update/{MISSING_UUID}", json=payload, headers=headers)
            invalid = client.patch("/calendar/condition/update/nie-uuid", json=payload, headers=headers)

        assert missing.status_code == 404
        assert invalid.status_code == 400


class TestApiSuperadminDeleteWorkCondition:
    def test_delete01_removes_condition(self, db_session: Session):
        condition = make_condition(db_session)
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete(f"/calendar/condition/delete/{condition.id}", headers=headers)

        assert response.status_code == 200
        assert db_session.query(WorkConditionChange).count() == 0
