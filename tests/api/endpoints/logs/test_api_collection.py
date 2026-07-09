from sqlalchemy.orm import Session

from api.endpoints.logs.collection import router as logs_collection_router
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.logs.helper import make_log


class TestApiSuperadminCollectionLogs:
    def test_collection01_superadmin_gets_logs(self, db_session: Session):
        make_log(db_session, description="tasks:create")
        make_log(db_session, description="auth:login")
        client = make_client(db_session, logs_collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/logs/collection/0", headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "SUCCESS"
        assert len(body["data"]) == 2

    def test_collection02_limit_works(self, db_session: Session):
        for _ in range(3):
            make_log(db_session)
        client = make_client(db_session, logs_collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/logs/collection/2", headers=headers)

        assert response.status_code == 200
        assert len(response.json()["data"]) == 2

    def test_collection03_admin_returns_403(self, db_session: Session):
        client = make_client(db_session, logs_collection_router)

        with authorized_as("admin") as headers:
            response = client.get("/logs/collection/0", headers=headers)

        assert response.status_code == 403
