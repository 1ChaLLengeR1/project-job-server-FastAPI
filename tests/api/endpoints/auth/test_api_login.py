import uuid
from unittest.mock import patch

from sqlalchemy.orm import Session

from api.endpoints.auth.login import router as login_router
from core.helper.password import hash_password
from core.repository.psql.user.response import UserResponse
from core.service.auth.tokens import encode_refresh_token
from database.psql.models.logs import Logs
from tests.api.helper import make_client
from tests.core.repository.psql.user.helper import create_test_user

PASSWORD = "TajneHaslo123!"


class TestApiPublicLogin:
    def test_login01_valid_credentials_returns_tokens(self, db_session: Session):
        user = create_test_user(db_session, password=hash_password(PASSWORD))
        client = make_client(db_session, login_router)

        response = client.post("/authentication/login", json={"username": user.username, "password": PASSWORD})

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "SUCCESS"
        assert body["data"]["id"] == str(user.id)
        assert body["data"]["access_token"] and body["data"]["refresh_token"]

    def test_login02_wrong_password_returns_401_generic_message(self, db_session: Session):
        user = create_test_user(db_session, password=hash_password(PASSWORD))
        client = make_client(db_session, login_router)

        bad_password = client.post(
            "/authentication/login", json={"username": user.username, "password": "zle"}
        )
        missing_user = client.post("/authentication/login", json={"username": "nie_ma", "password": "zle"})

        assert bad_password.status_code == 401 and missing_user.status_code == 401
        # brak enumeracji userów — identyczny komunikat
        assert bad_password.json()["data"]["message"] == missing_user.json()["data"]["message"]

    def test_login03_empty_username_returns_422(self, db_session: Session):
        client = make_client(db_session, login_router)

        response = client.post("/authentication/login", json={"username": "  ", "password": "x"})

        assert response.status_code == 422

    def test_login04_success_writes_audit_log(self, db_session: Session):
        user = create_test_user(db_session, password=hash_password(PASSWORD))
        client = make_client(db_session, login_router)

        client.post("/authentication/login", json={"username": user.username, "password": PASSWORD})

        log = db_session.query(Logs).filter(Logs.description == "auth:login").first()
        assert log is not None and log.username == user.username


class TestApiPublicAutomaticallyLogin:
    def test_refresh01_valid_token_returns_new_tokens(self, db_session: Session):
        user_id = str(uuid.uuid4())
        user = UserResponse(id=user_id, username="jan", type="user")
        client = make_client(db_session, login_router)

        with patch(
            "core.middleware.refresh_authorization.one_user_by_id_psql", return_value=(user, None, True)
        ):
            response = client.get(
                f"/authentication/automatically_login/{user_id}",
                headers={"X-Refresh-Token": encode_refresh_token(user_id)},
            )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "SUCCESS"
        assert body["data"]["id"] == user_id and body["data"]["access_token"]

    def test_refresh02_token_of_other_user_returns_401(self, db_session: Session):
        user_id = str(uuid.uuid4())
        client = make_client(db_session, login_router)

        response = client.get(
            f"/authentication/automatically_login/{user_id}",
            headers={"X-Refresh-Token": encode_refresh_token(str(uuid.uuid4()))},
        )

        assert response.status_code == 401
