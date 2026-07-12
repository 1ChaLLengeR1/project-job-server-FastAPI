from datetime import date
from unittest.mock import patch

from sqlalchemy.orm import Session

from api.endpoints.calendar.collection import router as collection_router
from api.endpoints.calendar.create import router as create_router
from api.endpoints.calendar.statistics import router as statistics_router
from api.response import ApiErrorData
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.calendar.helper import make_condition, make_work_day

HOLIDAYS_PATCH = "core.handler.calendar.create.fetch_public_holidays"
YEAR = date.today().year + 5


class TestApiSuperadminCreateCalendar:
    def test_create01_generates_year_with_mocked_holidays(self, db_session: Session):
        make_condition(db_session)
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers, patch(HOLIDAYS_PATCH, return_value=([], None, True)):
            response = client.post("/calendar/generate", json={"year": YEAR}, headers=headers)

        assert response.status_code == 201
        body = response.json()
        assert body["data"]["inserted_count"] in (365, 366)
        assert body["data"]["summary"]["year"] == YEAR

    def test_create02_duplicate_year_returns_409(self, db_session: Session):
        make_condition(db_session)
        make_work_day(db_session, day=date(YEAR, 3, 15))
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers, patch(HOLIDAYS_PATCH, return_value=([], None, True)):
            response = client.post("/calendar/generate", json={"year": YEAR}, headers=headers)

        assert response.status_code == 409

    def test_create03_holiday_api_failure_returns_502(self, db_session: Session):
        make_condition(db_session)
        client = make_client(db_session, create_router)
        external_error = ApiErrorData(
            message="timeout",
            type_module="fetch_public_holidays",
            type_error="external_service_error",
            key_type_error="ExternalService",
        )

        with authorized_as("superadmin") as headers, patch(HOLIDAYS_PATCH, return_value=(None, external_error, False)):
            response = client.post("/calendar/generate", json={"year": YEAR}, headers=headers)

        assert response.status_code == 502

    def test_create04_year_out_of_range_returns_422(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post("/calendar/generate", json={"year": 2200}, headers=headers)

        assert response.status_code == 422


class TestApiUserCollectionCalendar:
    def test_collection01_returns_month(self, db_session: Session):
        make_work_day(db_session, day=date(2030, 1, 10), hours_worked=8, hourly_rate=30)
        client = make_client(db_session, collection_router)

        with authorized_as("user") as headers:
            response = client.get("/calendar/collection?year=2030&month=1", headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body["data"]["month_name"] == "Styczeń"
        assert len(body["data"]["days"]) == 1

    def test_collection02_empty_month_returns_404(self, db_session: Session):
        client = make_client(db_session, collection_router)

        with authorized_as("user") as headers:
            response = client.get("/calendar/collection?year=2030&month=6", headers=headers)

        assert response.status_code == 404

    def test_collection03_invalid_month_returns_422(self, db_session: Session):
        client = make_client(db_session, collection_router)

        with authorized_as("user") as headers:
            response = client.get("/calendar/collection?year=2030&month=13", headers=headers)

        assert response.status_code == 422


class TestApiUserStatisticsCalendar:
    def test_statistics01_returns_year_aggregates(self, db_session: Session):
        make_work_day(db_session, day=date(2030, 1, 10), hours_worked=8, hourly_rate=30)
        client = make_client(db_session, statistics_router)

        with authorized_as("user") as headers:
            response = client.get("/calendar/statistics?year=2030", headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body["data"]["total_hours_worked"] == 8
        assert body["data"]["total_earnings"] == 240
