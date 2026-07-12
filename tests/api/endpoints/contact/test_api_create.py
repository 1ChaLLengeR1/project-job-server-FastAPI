from sqlalchemy.orm import Session

from api.endpoints.contact.create import router as create_router
from core.middleware.contact_token_authorization import CONTACT_TOKEN_HEADER
from core.service.contact.token import encode_contact_token
from database.psql.models.contact import ContactMessage
from database.psql.models.logs import Logs
from tests.api.helper import make_client

VALID_PAYLOAD = {
    "first_name": "Jan",
    "last_name": "Kowalski",
    "phone_number": "+48 500 600 700",
    "email": "jan@example.com",
    "description": "Pytanie o wycenę mieszkania",
}


def contact_headers(application: str = "portfolio", expires_minutes: int = 5) -> dict:
    return {CONTACT_TOKEN_HEADER: encode_contact_token(application, expires_minutes=expires_minutes)}


class TestApiPublicCreateContactMessage:
    def test_create01_valid_token_returns_201_and_saves_row(self, db_session: Session):
        client = make_client(db_session, create_router)

        response = client.post("/contact/messages/create", json=VALID_PAYLOAD, headers=contact_headers())

        assert response.status_code == 201
        body = response.json()
        assert body["status"] == "SUCCESS"
        assert body["data"]["first_name"] == "Jan" and body["data"]["status"] == "new"
        assert db_session.query(ContactMessage).count() == 1

    def test_create02_application_comes_from_token_claim(self, db_session: Session):
        client = make_client(db_session, create_router)

        response = client.post(
            "/contact/messages/create", json=VALID_PAYLOAD, headers=contact_headers(application="rentals-app")
        )

        assert response.json()["data"]["application"] == "rentals-app"
        row = db_session.query(ContactMessage).first()
        assert row.application == "rentals-app"

    def test_create03_no_token_returns_401(self, db_session: Session):
        client = make_client(db_session, create_router)

        response = client.post("/contact/messages/create", json=VALID_PAYLOAD)

        assert response.status_code == 401
        assert db_session.query(ContactMessage).count() == 0

    def test_create04_garbage_token_returns_401(self, db_session: Session):
        client = make_client(db_session, create_router)

        response = client.post(
            "/contact/messages/create", json=VALID_PAYLOAD, headers={CONTACT_TOKEN_HEADER: "abc.def.ghi"}
        )

        assert response.status_code == 401

    def test_create05_expired_token_returns_401(self, db_session: Session):
        client = make_client(db_session, create_router)

        response = client.post(
            "/contact/messages/create", json=VALID_PAYLOAD, headers=contact_headers(expires_minutes=-1)
        )

        assert response.status_code == 401

    def test_create06_invalid_payload_returns_422(self, db_session: Session):
        client = make_client(db_session, create_router)
        headers = contact_headers()

        empty_description = client.post(
            "/contact/messages/create", json={**VALID_PAYLOAD, "description": "   "}, headers=headers
        )
        bad_phone = client.post(
            "/contact/messages/create", json={**VALID_PAYLOAD, "phone_number": "zadzwoń"}, headers=headers
        )
        bad_email = client.post(
            "/contact/messages/create", json={**VALID_PAYLOAD, "email": "nie-email"}, headers=headers
        )

        assert empty_description.status_code == 422
        assert bad_phone.status_code == 422
        assert bad_email.status_code == 422

    def test_create07_optional_fields_can_be_omitted(self, db_session: Session):
        client = make_client(db_session, create_router)
        minimal = {"first_name": "Ania", "phone_number": "500600700", "description": "Proszę o kontakt"}

        response = client.post("/contact/messages/create", json=minimal, headers=contact_headers())

        assert response.status_code == 201
        assert response.json()["data"]["last_name"] is None
        assert response.json()["data"]["email"] is None

    def test_create08_public_create_writes_no_audit_log(self, db_session: Session):
        # endpoint publiczny — brak usera, brak wpisu w logs
        client = make_client(db_session, create_router)

        client.post("/contact/messages/create", json=VALID_PAYLOAD, headers=contact_headers())

        assert db_session.query(Logs).count() == 0
