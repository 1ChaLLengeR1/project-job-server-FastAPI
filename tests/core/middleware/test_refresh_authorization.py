import uuid
from unittest.mock import patch

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from core.data.user import UserData
from core.middleware.refresh_authorization import JWTRefreshAuthenticationMiddleware
from core.service.auth.tokens import encode_access_token, encode_refresh_token
from tests.core.middleware.helper import USER_ID, make_user_response, user_found, user_not_found

PATCH_TARGET = "core.middleware.refresh_authorization.one_user_by_id_psql"


def make_client() -> TestClient:
    app = FastAPI()

    @app.get("/refresh/{user_id}")
    def refresh(user_data: UserData = Depends(JWTRefreshAuthenticationMiddleware())):
        return user_data

    return TestClient(app, raise_server_exceptions=False)


class TestJWTRefreshAuthenticationMiddleware:
    def test_refresh01_valid_token_returns_user_data(self):
        user = make_user_response(username="jan", type="user")
        headers = {"X-Refresh-Token": encode_refresh_token(USER_ID)}

        with patch(PATCH_TARGET, return_value=user_found(user)):
            response = make_client().get(f"/refresh/{USER_ID}", headers=headers)

        assert response.status_code == 200
        assert response.json() == {"id": USER_ID, "username": "jan", "type": "user"}

    def test_refresh02_token_of_other_user_returns_401(self):
        other_id = str(uuid.uuid4())
        headers = {"X-Refresh-Token": encode_refresh_token(other_id)}

        response = make_client().get(f"/refresh/{USER_ID}", headers=headers)

        assert response.status_code == 401
        assert "does not belong" in response.json()["detail"]

    def test_refresh03_invalid_uuid_in_path_returns_400(self):
        headers = {"X-Refresh-Token": encode_refresh_token(USER_ID)}

        response = make_client().get("/refresh/nie-uuid", headers=headers)

        assert response.status_code == 400

    def test_refresh04_missing_header_returns_422(self):
        response = make_client().get(f"/refresh/{USER_ID}")

        assert response.status_code == 422

    def test_refresh05_access_token_rejected_as_refresh(self):
        headers = {"X-Refresh-Token": encode_access_token(USER_ID)}

        response = make_client().get(f"/refresh/{USER_ID}", headers=headers)

        assert response.status_code == 401

    def test_refresh06_missing_user_returns_401(self):
        headers = {"X-Refresh-Token": encode_refresh_token(USER_ID)}

        with patch(PATCH_TARGET, return_value=user_not_found()):
            response = make_client().get(f"/refresh/{USER_ID}", headers=headers)

        assert response.status_code == 401
