import uuid
from contextlib import contextmanager
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session

from api.exception_handlers import register_exception_handlers
from config.rate_limit import limiter, rate_limit_exceeded_handler
from core.repository.psql.user.response import UserResponse
from core.service.auth.tokens import encode_access_token
from database.psql.database import get_db


def make_client(db_session: Session, *routers) -> TestClient:
    """Świeża aplikacja per test: exception handlery, rate limiter, get_db
    nadpisany na sesję testową i tylko routery potrzebne w teście
    (wzorzec: docs/ARCHITEKTURA.md sekcja 12)."""
    app = FastAPI()
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    register_exception_handlers(app)

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    for router in routers:
        app.include_router(router)

    return TestClient(app, raise_server_exceptions=False)


@contextmanager
def authorized_as(role: str = "superadmin", *, user_id: str | None = None, username: str = "tester"):
    """Mock autoryzacji JWT: patchuje lookup usera w middleware i zwraca
    nagłówek Authorization z prawdziwym access tokenem (service auth)."""
    user_id = user_id or str(uuid.uuid4())
    user = UserResponse(id=user_id, username=username, type=role)

    with patch(
        "core.middleware.basic_authorization.one_user_by_id_psql",
        return_value=(user, None, True),
    ):
        yield {"Authorization": f"Bearer {encode_access_token(user_id)}"}
