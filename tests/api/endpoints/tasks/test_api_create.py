from sqlalchemy.orm import Session

from api.endpoints.tasks.create import router as create_router
from database.psql.models.logs import Logs
from database.psql.models.tasks import Tasks
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.user.helper import create_test_user


class TestApiSuperadminCreateTask:
    def test_create01_returns_201_and_saves_row(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post("/tasks/create", json={"description": "nowy", "time": 30}, headers=headers)

        assert response.status_code == 201
        body = response.json()
        assert body["status"] == "SUCCESS" and body["status_code"] == 201
        assert body["data"]["description"] == "nowy" and body["data"]["active"] is True
        assert db_session.query(Tasks).count() == 1

    def test_create02_invalid_payload_returns_422(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            empty_description = client.post(
                "/tasks/create", json={"description": "  ", "time": 30}, headers=headers
            )
            zero_time = client.post("/tasks/create", json={"description": "x", "time": 0}, headers=headers)

        assert empty_description.status_code == 422
        assert zero_time.status_code == 422

    def test_create03_no_token_returns_401(self, db_session: Session):
        client = make_client(db_session, create_router)

        response = client.post("/tasks/create", json={"description": "x", "time": 1})

        assert response.status_code == 401

    def test_create04_role_user_returns_403(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("user") as headers:
            response = client.post("/tasks/create", json={"description": "x", "time": 1}, headers=headers)

        assert response.status_code == 403

    def test_create05_writes_audit_log_for_real_user(self, db_session: Session):
        user = create_test_user(db_session, type="superadmin")
        client = make_client(db_session, create_router)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            client.post("/tasks/create", json={"description": "x", "time": 1}, headers=headers)

        log = db_session.query(Logs).filter(Logs.description == "tasks:create").first()
        assert log is not None and log.username == user.username
