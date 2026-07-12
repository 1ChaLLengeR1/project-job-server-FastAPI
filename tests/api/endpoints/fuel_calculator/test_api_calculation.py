from sqlalchemy.orm import Session

from api.endpoints.fuel_calculator.calculation import router as fuel_router
from tests.api.helper import authorized_as, make_client

PAYLOAD = {"way": 100, "fuel": 6.0, "combustion": 6.5, "remaining_values": 10}


class TestApiUserFuelCalculation:
    def test_calculation01_returns_price(self, db_session: Session):
        client = make_client(db_session, fuel_router)

        with authorized_as("user") as headers:
            response = client.post("/fuel/fuel_calculations", json=PAYLOAD, headers=headers)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "SUCCESS"
        assert body["data"]["price"] == 49.0
        assert "pattern" in body["data"]

    def test_calculation02_negative_way_returns_422(self, db_session: Session):
        client = make_client(db_session, fuel_router)

        with authorized_as("user") as headers:
            response = client.post(
                "/fuel/fuel_calculations", json={**PAYLOAD, "way": -5}, headers=headers
            )

        assert response.status_code == 422

    def test_calculation03_no_token_returns_401(self, db_session: Session):
        client = make_client(db_session, fuel_router)

        assert client.post("/fuel/fuel_calculations", json=PAYLOAD).status_code == 401
