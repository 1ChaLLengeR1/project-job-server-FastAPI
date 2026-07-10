from datetime import date
from uuid import uuid4

from sqlalchemy.orm import Session

from api.endpoints.rental.billing.close import router as close_router
from api.endpoints.rental.billing.collection import router as collection_router
from api.endpoints.rental.billing.create import router as create_router
from api.endpoints.rental.billing.delete import router as delete_router
from api.endpoints.rental.billing.one import router as one_router
from api.endpoints.rental.billing.preview import router as preview_router
from api.endpoints.rental.billing.update import router as update_router
from database.psql.models.logs import Logs
from database.psql.models.rentals import RentalMeterReading, RentalSettlement
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.rental.helper import (
    make_apartment,
    make_apartment_cost,
    make_billing_period,
    make_cost_type,
    make_meter,
    make_meter_reading,
    make_settlement,
    make_settlement_item,
    make_tenancy,
)
from tests.core.repository.psql.user.helper import create_test_user


class TestApiRentalPeriodCreate:
    def test_period01_create_returns_201_and_prefills_readings(self, db_session: Session):
        meter = make_meter(db_session)
        make_meter(db_session, is_active=False)
        previous_period = make_billing_period(db_session, period_month=date(2026, 5, 1))
        make_meter_reading(db_session, period=previous_period, meter=meter, previous_value=100, current_value=250)
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/rentals/periods/create",
                json={"period_month": "2026-06-01", "electricity_bill_amount": 899.48},
                headers=headers,
            )

        assert response.status_code == 201
        body = response.json()["data"]
        assert body["status"] == "draft" and body["water_rate"] == 9.00
        readings = db_session.query(RentalMeterReading).filter(RentalMeterReading.period_id == body["id"]).all()
        assert len(readings) == 1  # tylko aktywny licznik
        assert float(readings[0].previous_value) == 250  # prefill "Ostatnio" = "Teraz" z poprzedniego okresu

    def test_period02_create_duplicate_month_returns_409(self, db_session: Session):
        make_billing_period(db_session, period_month=date(2026, 6, 1))
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post("/rentals/periods/create", json={"period_month": "2026-06-01"}, headers=headers)

        assert response.status_code == 409

    def test_period03_no_token_401_and_role_user_403(self, db_session: Session):
        client = make_client(db_session, create_router)

        no_token = client.post("/rentals/periods/create", json={"period_month": "2026-06-01"})
        with authorized_as("user") as headers:
            wrong_role = client.post("/rentals/periods/create", json={"period_month": "2026-06-01"}, headers=headers)

        assert no_token.status_code == 401
        assert wrong_role.status_code == 403


class TestApiRentalPeriodsRead:
    def test_periods01_collection_filters_by_status(self, db_session: Session):
        make_billing_period(db_session, period_month=date(2026, 5, 1), status="closed")
        make_billing_period(db_session, period_month=date(2026, 6, 1), status="draft")
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            all_rows = client.get("/rentals/periods/collection", headers=headers)
            drafts = client.get("/rentals/periods/collection", params={"status": "draft"}, headers=headers)

        assert len(all_rows.json()["data"]) == 2
        draft_rows = drafts.json()["data"]
        assert len(draft_rows) == 1 and draft_rows[0]["status"] == "draft"

    def test_periods02_one_returns_period_and_404_for_missing(self, db_session: Session):
        period = make_billing_period(db_session)
        client = make_client(db_session, one_router)

        with authorized_as("superadmin") as headers:
            found = client.get(f"/rentals/periods/one/{period.id}", headers=headers)
            missing = client.get(f"/rentals/periods/one/{uuid4()}", headers=headers)

        assert found.status_code == 200 and found.json()["data"]["electricity_rate"] == 1.05
        assert missing.status_code == 404


class TestApiRentalPeriodUpdate:
    def test_period_update01_draft_returns_200(self, db_session: Session):
        period = make_billing_period(db_session)
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.put(
                f"/rentals/periods/update/{period.id}",
                json={
                    "electricity_bill_amount": 950.00,
                    "electricity_rate": 1.10,
                    "electricity_rate_is_manual": True,
                    "water_rate": 10.00,
                    "note": "korekta rachunku",
                },
                headers=headers,
            )

        assert response.status_code == 200
        body = response.json()["data"]
        assert body["water_rate"] == 10.00 and body["electricity_rate_is_manual"] is True

    def test_period_update02_closed_returns_409(self, db_session: Session):
        period = make_billing_period(db_session, status="closed")
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.put(
                f"/rentals/periods/update/{period.id}",
                json={"electricity_rate_is_manual": False, "water_rate": 9.00},
                headers=headers,
            )

        assert response.status_code == 409


class TestApiRentalMeterReadings:
    def test_reading01_create_returns_201(self, db_session: Session):
        period = make_billing_period(db_session)
        meter = make_meter(db_session)
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/rentals/readings/create",
                json={
                    "period_id": str(period.id),
                    "meter_id": str(meter.id),
                    "previous_value": 5621.26,
                    "current_value": 5938.86,
                },
                headers=headers,
            )

        assert response.status_code == 201
        assert response.json()["data"]["current_value"] == 5938.86

    def test_reading02_collection_by_period_and_invalid_uuid(self, db_session: Session):
        period = make_billing_period(db_session)
        make_meter_reading(db_session, period=period)
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            rows = client.get(f"/rentals/readings/collection/{period.id}", headers=headers)
            bad_uuid = client.get("/rentals/readings/collection/not-a-uuid", headers=headers)

        assert rows.status_code == 200 and len(rows.json()["data"]) == 1
        assert bad_uuid.status_code == 400

    def test_reading03_update_and_delete(self, db_session: Session):
        reading = make_meter_reading(db_session)
        client = make_client(db_session, update_router, delete_router)

        with authorized_as("superadmin") as headers:
            updated = client.put(
                f"/rentals/readings/update/{reading.id}",
                json={"previous_value": 100, "current_value": 200, "error_correction": 1},
                headers=headers,
            )
            deleted = client.delete(f"/rentals/readings/delete/{reading.id}", headers=headers)

        assert updated.status_code == 200 and updated.json()["data"]["error_correction"] == 1
        assert deleted.status_code == 200
        assert db_session.query(RentalMeterReading).count() == 0


class TestApiRentalPeriodPreviewCloseReopen:
    def _seed_small_period(self, db_session: Session):
        """Jedno mieszkanie: 100 kWh x (105 zł / 100 kWh) = 105 zł prądu,
        śmieci 2 os. x 35 zł = 70 zł, czynsz 1000 zł."""
        apartment = make_apartment(db_session, name="Pokój Łukasza")
        make_tenancy(db_session, apartment=apartment, rent_amount=1000.00, persons_count=2)
        smieci = make_cost_type(db_session, name="śmieci", charge_type="per_person")
        make_apartment_cost(db_session, apartment=apartment, cost_type=smieci, amount=35.00)
        meter = make_meter(db_session, apartment=apartment)
        period = make_billing_period(
            db_session, period_month=date(2026, 6, 1), electricity_bill_amount=105.00, electricity_rate=None
        )
        make_meter_reading(db_session, period=period, meter=meter, previous_value=100, current_value=200)
        return apartment, period

    def test_preview01_returns_calculation_without_saving(self, db_session: Session):
        apartment, period = self._seed_small_period(db_session)
        client = make_client(db_session, preview_router)

        with authorized_as("superadmin") as headers:
            response = client.post(f"/rentals/periods/preview/{period.id}", json={"adjustments": []}, headers=headers)

        assert response.status_code == 200
        body = response.json()["data"]
        assert body["electricity_rate"] == 1.05  # 105 zł / 100 kWh
        settlement = body["settlements"][0]["settlement"]
        assert settlement["electricity_cost"] == 105.00
        assert settlement["total_media_amount"] == 175.00  # prąd 105 + śmieci 70
        assert settlement["total_amount"] == 1175.00
        assert db_session.query(RentalSettlement).count() == 0  # preview nic nie zapisuje

    def test_preview02_missing_period_404_and_invalid_uuid_400(self, db_session: Session):
        client = make_client(db_session, preview_router)

        with authorized_as("superadmin") as headers:
            missing = client.post(f"/rentals/periods/preview/{uuid4()}", json={"adjustments": []}, headers=headers)
            bad_uuid = client.post("/rentals/periods/preview/not-a-uuid", json={"adjustments": []}, headers=headers)

        assert missing.status_code == 404
        assert bad_uuid.status_code == 400

    def test_close01_saves_snapshots_and_blocks_second_close(self, db_session: Session):
        apartment, period = self._seed_small_period(db_session)
        client = make_client(db_session, close_router)

        with authorized_as("superadmin") as headers:
            closed = client.post(
                f"/rentals/periods/close/{period.id}",
                json={"adjustments": [{"apartment_id": str(apartment.id), "name": "nadpłata", "amount": -19}]},
                headers=headers,
            )
            second_close = client.post(f"/rentals/periods/close/{period.id}", json={"adjustments": []}, headers=headers)

        assert closed.status_code == 200
        body = closed.json()["data"]
        assert body["period"]["status"] == "closed"
        settlement = body["settlements"][0]["settlement"]
        assert settlement["total_media_amount"] == 156.00  # 175 - 19 nadpłaty
        assert db_session.query(RentalSettlement).count() == 1
        assert second_close.status_code == 409

    def test_close02_writes_audit_log(self, db_session: Session):
        _, period = self._seed_small_period(db_session)
        user = create_test_user(db_session, type="superadmin")
        client = make_client(db_session, close_router)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            client.post(f"/rentals/periods/close/{period.id}", json={"adjustments": []}, headers=headers)

        log = db_session.query(Logs).filter(Logs.description == "rental:close_billing_period").first()
        assert log is not None and log.username == user.username

    def test_reopen01_deletes_snapshots_and_blocks_draft(self, db_session: Session):
        _, period = self._seed_small_period(db_session)
        client = make_client(db_session, close_router)

        with authorized_as("superadmin") as headers:
            client.post(f"/rentals/periods/close/{period.id}", json={"adjustments": []}, headers=headers)
            reopened = client.post(f"/rentals/periods/reopen/{period.id}", headers=headers)
            reopen_draft = client.post(f"/rentals/periods/reopen/{period.id}", headers=headers)

        assert reopened.status_code == 200 and reopened.json()["data"]["status"] == "draft"
        assert db_session.query(RentalSettlement).count() == 0
        assert reopen_draft.status_code == 409

    def test_delete01_period_removes_readings(self, db_session: Session):
        _, period = self._seed_small_period(db_session)
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete(f"/rentals/periods/delete/{period.id}", headers=headers)

        assert response.status_code == 200
        assert db_session.query(RentalMeterReading).count() == 0


class TestApiRentalSettlements:
    def test_settlements01_collection_filters_by_period(self, db_session: Session):
        period = make_billing_period(db_session, period_month=date(2026, 6, 1))
        settlement = make_settlement(db_session, period=period)
        make_settlement_item(db_session, settlement=settlement)
        make_settlement(db_session, period=make_billing_period(db_session, period_month=date(2026, 7, 1)))
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get(
                "/rentals/settlements/collection", params={"period_id": str(period.id)}, headers=headers
            )

        rows = response.json()["data"]
        assert len(rows) == 1
        assert rows[0]["total_amount"] == 1629.00
        assert rows[0]["items"][0]["amount"] == 70.00

    def test_settlements02_one_returns_settlement_and_404(self, db_session: Session):
        settlement = make_settlement(db_session)
        client = make_client(db_session, one_router)

        with authorized_as("superadmin") as headers:
            found = client.get(f"/rentals/settlements/one/{settlement.id}", headers=headers)
            missing = client.get(f"/rentals/settlements/one/{uuid4()}", headers=headers)

        assert found.status_code == 200 and found.json()["data"]["rent_amount"] == 1100.00
        assert missing.status_code == 404
