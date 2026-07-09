from datetime import date

from sqlalchemy.orm import Session

from api.endpoints.calendar.days.update import router as days_router
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.calendar.helper import make_work_day


class TestApiSuperadminUpdateDayById:
    def test_update_by_id01_changes_day(self, db_session: Session):
        work_day = make_work_day(db_session, day=date(2030, 1, 10))
        client = make_client(db_session, days_router)

        with authorized_as("superadmin") as headers:
            response = client.patch(
                f"/calendar/day/work/update/{work_day.id}",
                json={"norm_hours": 7, "hours_worked": 5.5, "hourly_rate": 40},
                headers=headers,
            )

        assert response.status_code == 200
        assert response.json()["data"]["hours_worked"] == 5.5

    def test_update_by_id02_hours_above_24_returns_422(self, db_session: Session):
        work_day = make_work_day(db_session, day=date(2030, 1, 10))
        client = make_client(db_session, days_router)

        with authorized_as("superadmin") as headers:
            response = client.patch(
                f"/calendar/day/work/update/{work_day.id}",
                json={"norm_hours": 8, "hours_worked": 25, "hourly_rate": 30},
                headers=headers,
            )

        assert response.status_code == 422


class TestApiSuperadminUpdateDaysRange:
    def test_range01_updates_days(self, db_session: Session):
        for day_number in (10, 11, 12):
            make_work_day(db_session, day=date(2030, 1, day_number), hours_worked=0)
        client = make_client(db_session, days_router)
        payload = {
            "year": 2030, "month": 1, "start_day": 10, "end_day": 12,
            "norm_hours": 8, "hours_worked": 8, "hourly_rate": 33,
        }

        with authorized_as("superadmin") as headers:
            response = client.patch("/calendar/days/work/update", json=payload, headers=headers)

        assert response.status_code == 200
        assert response.json()["data"]["updated_count"] == 3

    def test_range02_start_after_end_returns_422(self, db_session: Session):
        client = make_client(db_session, days_router)
        payload = {
            "year": 2030, "month": 1, "start_day": 10, "end_day": 5,
            "norm_hours": 8, "hours_worked": 8, "hourly_rate": 33,
        }

        with authorized_as("superadmin") as headers:
            response = client.patch("/calendar/days/work/update", json=payload, headers=headers)

        assert response.status_code == 422


class TestApiSuperadminUpdateDaysSalary:
    def test_salary01_recalculates_rate(self, db_session: Session):
        make_work_day(db_session, day=date(2030, 1, 10), hours_worked=8, norm_hours=8)
        make_work_day(db_session, day=date(2030, 1, 11), hours_worked=2, norm_hours=8)
        client = make_client(db_session, days_router)

        with authorized_as("superadmin") as headers:
            response = client.patch(
                "/calendar/days/work/update/salary",
                json={"year": 2030, "month": 1, "salary": 500},
                headers=headers,
            )

        assert response.status_code == 200
        assert response.json()["data"]["calculated_hourly_rate"] == 50.0

    def test_salary02_no_days_returns_404(self, db_session: Session):
        client = make_client(db_session, days_router)

        with authorized_as("superadmin") as headers:
            response = client.patch(
                "/calendar/days/work/update/salary",
                json={"year": 2030, "month": 2, "salary": 500},
                headers=headers,
            )

        assert response.status_code == 404
