from sqlalchemy.orm import Session

from api.endpoints.patryk_router.calculator_work.calculator import router as calculations_router
from api.endpoints.patryk_router.calculator_work.one import router as one_router
from api.endpoints.patryk_router.calculator_work.update import router as update_router
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.patryk.helper import make_calculator_keys

CALCULATION_PAYLOAD = {
    "gross_sales": 100.0,
    "gross_purchase": 50.0,
    "provision": 10.0,
    "distinction": 2.0,
    "referrer": "dpd",
}


class TestApiAdminOneCalculatorKeys:
    def test_one01_returns_keys(self, db_session: Session):
        keys = make_calculator_keys(db_session, vat=0.23)
        client = make_client(db_session, one_router)

        with authorized_as("admin") as headers:
            response = client.get("/calculator_work/calculator_keys", headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body["data"]["id"] == str(keys.id)
        assert body["data"]["vat"] == 0.23

    def test_one02_empty_table_returns_404(self, db_session: Session):
        client = make_client(db_session, one_router)

        with authorized_as("admin") as headers:
            response = client.get("/calculator_work/calculator_keys", headers=headers)

        assert response.status_code == 404

    def test_one03_role_user_returns_403_superadmin_passes(self, db_session: Session):
        make_calculator_keys(db_session)
        client = make_client(db_session, one_router)

        with authorized_as("user") as headers:
            assert client.get("/calculator_work/calculator_keys", headers=headers).status_code == 403
        with authorized_as("superadmin") as headers:
            assert client.get("/calculator_work/calculator_keys", headers=headers).status_code == 200


class TestApiAdminUpdateCalculatorKeys:
    def test_update01_changes_keys(self, db_session: Session):
        keys = make_calculator_keys(db_session)
        client = make_client(db_session, update_router)
        payload = {
            "id": str(keys.id),
            "income_tax": 0.19,
            "vat": 0.23,
            "inpost_parcel_locker": 13.5,
            "inpost_courier": 16.5,
            "inpost_cash_of_delivery_courier": 20.5,
            "dpd": 15.5,
            "allegro_matt": 10.5,
            "without_smart": 12.5,
        }

        with authorized_as("admin") as headers:
            response = client.put("/calculator_work/calculator_keys/update", json=payload, headers=headers)

        assert response.status_code == 200
        assert response.json()["data"]["income_tax"] == 0.19

    def test_update02_invalid_uuid_returns_422(self, db_session: Session):
        client = make_client(db_session, update_router)
        payload = {
            "id": "nie-uuid",
            "income_tax": 0.1,
            "vat": 0.2,
            "inpost_parcel_locker": 1,
            "inpost_courier": 2,
            "inpost_cash_of_delivery_courier": 3,
            "dpd": 4,
            "allegro_matt": 5,
            "without_smart": 6,
        }

        with authorized_as("admin") as headers:
            response = client.put("/calculator_work/calculator_keys/update", json=payload, headers=headers)

        assert response.status_code == 422


class TestApiAdminCalculations:
    def test_calculations01_returns_profit(self, db_session: Session):
        make_calculator_keys(db_session)
        client = make_client(db_session, calculations_router)

        with authorized_as("admin") as headers:
            response = client.post(
                "/calculator_work/calculator_keys/calculations", json=CALCULATION_PAYLOAD, headers=headers
            )

        assert response.status_code == 200
        body = response.json()
        assert set(body["data"].keys()) == {"brutto", "na_czysto", "zysk_procentowy"}

    def test_calculations02_unknown_referrer_returns_422(self, db_session: Session):
        client = make_client(db_session, calculations_router)

        with authorized_as("admin") as headers:
            response = client.post(
                "/calculator_work/calculator_keys/calculations",
                json={**CALCULATION_PAYLOAD, "referrer": "golab"},
                headers=headers,
            )

        assert response.status_code == 422

    def test_calculations03_missing_keys_returns_404(self, db_session: Session):
        client = make_client(db_session, calculations_router)

        with authorized_as("admin") as headers:
            response = client.post(
                "/calculator_work/calculator_keys/calculations", json=CALCULATION_PAYLOAD, headers=headers
            )

        assert response.status_code == 404
