from sqlalchemy.orm import Session

from api.endpoints.tasks.collection import router as collection_router
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.tasks.helper import make_task


class TestApiUserCollectionTasks:
    def test_collection01_returns_active_tasks(self, db_session: Session):
        make_task(db_session, description="aktywny", active=True)
        make_task(db_session, description="wykonany", active=False)
        client = make_client(db_session, collection_router)

        with authorized_as("user") as headers:
            response = client.get("/tasks/collection", headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "SUCCESS"
        assert [task["description"] for task in body["data"]] == ["aktywny"]

    def test_collection02_active_false_filter(self, db_session: Session):
        make_task(db_session, active=True)
        make_task(db_session, description="wykonany", active=False)
        client = make_client(db_session, collection_router)

        with authorized_as("user") as headers:
            response = client.get("/tasks/collection?active=false", headers=headers)

        assert response.status_code == 200
        assert [task["description"] for task in response.json()["data"]] == ["wykonany"]

    def test_collection03_no_token_returns_401(self, db_session: Session):
        client = make_client(db_session, collection_router)

        assert client.get("/tasks/collection").status_code == 401
