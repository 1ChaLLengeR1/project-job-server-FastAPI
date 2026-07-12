from unittest.mock import patch

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from core.data.user import UserData
from core.middleware.basic_authorization import JWTBasicAuthenticationMiddleware
from core.service.auth.tokens import encode_access_token, encode_refresh_token
from tests.core.middleware.helper import USER_ID, make_user_response, user_found, user_not_found

PATCH_TARGET = "core.middleware.basic_authorization.one_user_by_id_psql"


def make_client() -> TestClient:
    app = FastAPI()

    @app.get("/admin_only")
    def admin_only(user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["admin"]))):
        return user_data

    @app.get("/any_logged")
    def any_logged(user_data: UserData = Depends(JWTBasicAuthenticationMiddleware())):
        return user_data

    return TestClient(app, raise_server_exceptions=False)


def auth_header(user_id: str = USER_ID) -> dict:
    return {"Authorization": f"Bearer {encode_access_token(user_id)}"}


class TestJWTBasicAuthenticationMiddleware:
    def test_auth01_no_token_returns_401(self):
        response = make_client().get("/any_logged")

        assert response.status_code == 401

    def test_auth02_garbage_token_returns_401(self):
        response = make_client().get("/any_logged", headers={"Authorization": "Bearer abc.def.ghi"})

        assert response.status_code == 401

    def test_auth03_valid_token_returns_user_data(self):
        user = make_user_response(username="jan", type="user")

        with patch(PATCH_TARGET, return_value=user_found(user)):
            response = make_client().get("/any_logged", headers=auth_header())

        assert response.status_code == 200
        assert response.json() == {"id": USER_ID, "username": "jan", "type": "user"}

    def test_auth04_missing_user_returns_401(self):
        with patch(PATCH_TARGET, return_value=user_not_found()):
            response = make_client().get("/any_logged", headers=auth_header())

        assert response.status_code == 401

    def test_auth05_role_user_on_admin_endpoint_returns_403(self):
        user = make_user_response(type="user")

        with patch(PATCH_TARGET, return_value=user_found(user)):
            response = make_client().get("/admin_only", headers=auth_header())

        assert response.status_code == 403

    def test_auth06_role_admin_passes_admin_endpoint(self):
        user = make_user_response(type="admin")

        with patch(PATCH_TARGET, return_value=user_found(user)):
            response = make_client().get("/admin_only", headers=auth_header())

        assert response.status_code == 200

    def test_auth07_superadmin_passes_every_role_check(self):
        user = make_user_response(type="superadmin")

        with patch(PATCH_TARGET, return_value=user_found(user)):
            response = make_client().get("/admin_only", headers=auth_header())

        assert response.status_code == 200

    def test_auth08_refresh_token_rejected_as_access(self):
        headers = {"Authorization": f"Bearer {encode_refresh_token(USER_ID)}"}

        response = make_client().get("/any_logged", headers=headers)

        assert response.status_code == 401
