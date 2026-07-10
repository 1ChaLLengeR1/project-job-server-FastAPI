from uuid import uuid4

from sqlalchemy.orm import Session

from api.endpoints.contact.collection import router as collection_router
from api.endpoints.contact.delete import router as delete_router
from api.endpoints.contact.one import router as one_router
from api.endpoints.contact.update import router as update_router
from database.psql.models.contact import ContactMessage
from database.psql.models.logs import Logs
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.contact.helper import make_contact_message
from tests.core.repository.psql.user.helper import create_test_user


class TestApiSuperadminCollectionContactMessages:
    def test_collection01_returns_messages_with_filters(self, db_session: Session):
        make_contact_message(db_session, application="portfolio", status="new")
        make_contact_message(db_session, application="rentals-app", status="closed")
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            all_rows = client.get("/contact/messages/collection", headers=headers)
            by_application = client.get(
                "/contact/messages/collection", params={"application": "portfolio"}, headers=headers
            )
            by_status = client.get("/contact/messages/collection", params={"status": "closed"}, headers=headers)

        assert len(all_rows.json()["data"]) == 2
        assert [row["application"] for row in by_application.json()["data"]] == ["portfolio"]
        assert [row["status"] for row in by_status.json()["data"]] == ["closed"]

    def test_collection02_no_token_401_and_role_user_403(self, db_session: Session):
        client = make_client(db_session, collection_router)

        no_token = client.get("/contact/messages/collection")
        with authorized_as("user") as headers:
            wrong_role = client.get("/contact/messages/collection", headers=headers)

        assert no_token.status_code == 401
        assert wrong_role.status_code == 403

    def test_collection03_writes_audit_log(self, db_session: Session):
        user = create_test_user(db_session, type="superadmin")
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            client.get("/contact/messages/collection", headers=headers)

        log = db_session.query(Logs).filter(Logs.description == "contact:collection_messages").first()
        assert log is not None and log.username == user.username


class TestApiSuperadminOneContactMessage:
    def test_one01_returns_message_404_for_missing_400_for_bad_uuid(self, db_session: Session):
        message = make_contact_message(db_session, description="Pytanie o garaż")
        client = make_client(db_session, one_router)

        with authorized_as("superadmin") as headers:
            found = client.get(f"/contact/messages/one/{message.id}", headers=headers)
            missing = client.get(f"/contact/messages/one/{uuid4()}", headers=headers)
            bad_uuid = client.get("/contact/messages/one/not-a-uuid", headers=headers)

        assert found.status_code == 200 and found.json()["data"]["description"] == "Pytanie o garaż"
        assert missing.status_code == 404
        assert bad_uuid.status_code == 400


class TestApiSuperadminUpdateContactMessageStatus:
    def test_update01_changes_status_and_writes_audit_log(self, db_session: Session):
        user = create_test_user(db_session, type="superadmin")
        message = make_contact_message(db_session, status="new")
        client = make_client(db_session, update_router)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            response = client.put(
                f"/contact/messages/update/status/{message.id}", json={"status": "read"}, headers=headers
            )

        assert response.status_code == 200
        assert response.json()["data"]["status"] == "read"
        log = db_session.query(Logs).filter(Logs.description == "contact:update_message_status").first()
        assert log is not None

    def test_update02_invalid_status_returns_422(self, db_session: Session):
        message = make_contact_message(db_session)
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.put(
                f"/contact/messages/update/status/{message.id}", json={"status": "archived"}, headers=headers
            )

        assert response.status_code == 422

    def test_update03_missing_message_returns_404(self, db_session: Session):
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.put(
                f"/contact/messages/update/status/{uuid4()}", json={"status": "read"}, headers=headers
            )

        assert response.status_code == 404


class TestApiSuperadminDeleteContactMessage:
    def test_delete01_removes_row(self, db_session: Session):
        message = make_contact_message(db_session)
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete(f"/contact/messages/delete/{message.id}", headers=headers)

        assert response.status_code == 200
        assert db_session.query(ContactMessage).count() == 0

    def test_delete02_missing_message_returns_404(self, db_session: Session):
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete(f"/contact/messages/delete/{uuid4()}", headers=headers)

        assert response.status_code == 404
