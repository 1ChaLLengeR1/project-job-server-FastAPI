from sqlalchemy.orm import Session

from api.endpoints.auth.login import router as login_router
from api.endpoints.tasks.collection import router as tasks_collection_router
from config.rate_limit import limiter
from tests.api.helper import authorized_as, make_client


class TestRateLimitIntegration:
    def test_rate_limit01_login_returns_429_after_limit(self, db_session: Session):
        """Integracja endpoint + slowapi: RATE_LIMIT_AUTH = 10/minute po IP."""
        client = make_client(db_session, login_router)
        limiter.reset()
        limiter.enabled = True
        try:
            statuses = [
                client.post("/authentication/login", json={"username": "nie_ma", "password": "x"}).status_code
                for _ in range(11)
            ]

            assert statuses[:10] == [401] * 10
            assert statuses[10] == 429

            response = client.post("/authentication/login", json={"username": "nie_ma", "password": "x"})
            body = response.json()
            assert body["status"] == "ERROR" and body["status_code"] == 429
            assert body["data"]["type_error"] == "rate_limit_exceeded"
        finally:
            limiter.enabled = False
            limiter.reset()

    def test_rate_limit02_authorized_endpoint_keyed_per_user(self, db_session: Session):
        """RATE_LIMIT_READ = 120/minute z kluczem per user — w limicie wszystko przechodzi."""
        client = make_client(db_session, tasks_collection_router)
        limiter.reset()
        limiter.enabled = True
        try:
            with authorized_as("user") as headers:
                statuses = [client.get("/tasks/collection", headers=headers).status_code for _ in range(5)]

            assert statuses == [200] * 5
        finally:
            limiter.enabled = False
            limiter.reset()
