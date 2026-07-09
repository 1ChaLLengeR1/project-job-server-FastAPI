from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from api.endpoints.tasks.statistics import router as statistics_router
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.tasks.helper import make_task


class TestApiUserTaskStatistics:
    def test_statistics01_returns_aggregates_for_range(self, db_session: Session):
        make_task(db_session, time=30, active=False)
        make_task(db_session, time=45, active=False)
        client = make_client(db_session, statistics_router)
        start = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
        end = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")

        with authorized_as("user") as headers:
            response = client.get(f"/tasks/statistics?start_date={start}&end_date={end}", headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body["data"]["total_tasks"] == 2
        assert body["data"]["total_time"] == 75

    def test_statistics02_no_params_defaults_to_now(self, db_session: Session):
        client = make_client(db_session, statistics_router)

        with authorized_as("user") as headers:
            response = client.get("/tasks/statistics", headers=headers)

        assert response.status_code == 200
        assert response.json()["data"]["total_tasks"] == 0
