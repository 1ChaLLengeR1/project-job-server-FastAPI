from sqlalchemy.orm import Session

from api.endpoints.tasks.delete import router as delete_router
from database.psql.models.tasks import Tasks
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.tasks.helper import make_task

MISSING_UUID = "6fa459ea-ee8a-4ca4-894e-db77e160355e"


class TestApiSuperadminDeleteTask:
    def test_delete01_removes_task(self, db_session: Session):
        task = make_task(db_session)
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete(f"/tasks/delete/{task.id}", headers=headers)

        assert response.status_code == 200
        assert db_session.query(Tasks).count() == 0

    def test_delete02_missing_task_returns_404(self, db_session: Session):
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete(f"/tasks/delete/{MISSING_UUID}", headers=headers)

        assert response.status_code == 404

    def test_delete03_invalid_uuid_returns_400(self, db_session: Session):
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete("/tasks/delete/nie-uuid", headers=headers)

        assert response.status_code == 400
        assert response.json()["data"]["type_error"] == "validation_error"
