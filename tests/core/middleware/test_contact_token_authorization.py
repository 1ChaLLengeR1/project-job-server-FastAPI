from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from core.middleware.contact_token_authorization import CONTACT_TOKEN_HEADER, ContactTokenAuthenticationMiddleware
from core.service.auth.tokens import encode_access_token
from core.service.contact.token import encode_contact_token


def make_client() -> TestClient:
    app = FastAPI()

    @app.post("/public_contact")
    def public_contact(application: str = Depends(ContactTokenAuthenticationMiddleware())):
        return {"application": application}

    return TestClient(app, raise_server_exceptions=False)


class TestContactTokenAuthenticationMiddleware:
    def test_contact_auth01_no_header_returns_401(self):
        response = make_client().post("/public_contact")

        assert response.status_code == 401

    def test_contact_auth02_garbage_token_returns_401(self):
        response = make_client().post("/public_contact", headers={CONTACT_TOKEN_HEADER: "abc.def.ghi"})

        assert response.status_code == 401

    def test_contact_auth03_valid_token_returns_application(self):
        token = encode_contact_token("portfolio")

        response = make_client().post("/public_contact", headers={CONTACT_TOKEN_HEADER: token})

        assert response.status_code == 200
        assert response.json() == {"application": "portfolio"}

    def test_contact_auth04_expired_token_returns_401(self):
        token = encode_contact_token("portfolio", expires_minutes=-1)

        response = make_client().post("/public_contact", headers={CONTACT_TOKEN_HEADER: token})

        assert response.status_code == 401

    def test_contact_auth05_user_access_token_returns_401(self):
        # token JWT usera (inny sekret) nie przechodzi jako token kontaktowy
        token = encode_access_token("11111111-1111-4111-8111-111111111111")

        response = make_client().post("/public_contact", headers={CONTACT_TOKEN_HEADER: token})

        assert response.status_code == 401
