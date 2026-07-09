from sqlalchemy.orm import Session

from api.endpoints.tasks.update import router as update_router
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.tasks.helper import make_task

MISSING_UUID = "6fa459ea-ee8a-4ca4-894e-db77e160355e"


class TestApiSuperadminUpdateTask:
    def test_update01_changes_task(self, db_session: Session):
        task = make_task(db_session, description="stary", time=10)
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.patch(
                f"/tasks/update/{task.id}", json={"description": "nowy", "time": 20}, headers=headers
            )

        assert response.status_code == 200
        assert response.json()["data"]["description"] == "nowy"

    def test_update02_missing_task_returns_404(self, db_session: Session):
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.patch(
                f"/tasks/update/{MISSING_UUID}", json={"description": "x", "time": 1}, headers=headers
            )

        assert response.status_code == 404
        assert response.json()["data"]["key_type_error"] == "NotFound"

    def test_update03_invalid_uuid_returns_400(self, db_session: Session):
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.patch(
                "/tasks/update/nie-uuid", json={"description": "x", "time": 1}, headers=headers
            )

        assert response.status_code == 400


class TestApiSuperadminUpdateTaskActive:
    def test_update_active01_changes_flag(self, db_session: Session):
        task = make_task(db_session, active=True)
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.patch(
                f"/tasks/update/active/{task.id}", json={"active": False}, headers=headers
            )

        assert response.status_code == 200
        assert response.json()["data"]["active"] is False

    def test_update_active02_role_user_returns_403(self, db_session: Session):
        task = make_task(db_session)
        client = make_client(db_session, update_router)

        with authorized_as("user") as headers:
            response = client.patch(
                f"/tasks/update/active/{task.id}", json={"active": False}, headers=headers
            )

        assert response.status_code == 403
