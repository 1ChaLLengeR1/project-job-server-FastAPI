"""Test API init/update/delete plikow - realny S3, bez mockow poza JWT
(full_integration). Wszystko przez HTTP (TestClient): `authorized_as` mockuje
tylko lookup usera w JWT middleware (jak w istniejacych testach e2e), reszta -
baza (`db_session`) i S3 - jest prawdziwa.
"""

from pathlib import Path

import pytest
import requests
from botocore.exceptions import ClientError

from api.endpoints.file.delete import router as delete_router
from api.endpoints.file.init import router as init_router
from api.endpoints.file.metadata import router as metadata_router
from api.endpoints.file.update import router as update_router
from config.settings import settings
from core.infra.s3.config import get_s3_client
from database.psql.models.file import File
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.user.helper import create_test_user

ROUTERS = (init_router, update_router, delete_router, metadata_router)
IMAGE_PATH = Path(__file__).resolve().parents[3] / "files_for_tests" / "Patryk, fortnite,naruto.png"


def _init_and_upload(client, headers, image_bytes: bytes, s3_client, *, name: str) -> dict:
    """Pomocnik: POST /files/init + prawdziwy PUT bajtow na S3. Zwraca dane z
    odpowiedzi init (file_id, s3_key doczytany z bazy nie jest tu potrzebny -
    wolajacy sam sobie doda s3_key do listy sprzatania, jesli chce)."""
    response = client.post(
        "/files/init",
        json={
            "name": name,
            "original_name": name,
            "size": len(image_bytes),
            "mime_type": "image/png",
            "file_type": "photo",
            "catalog": "tests/api_init_update_delete",
        },
        headers=headers,
    )
    assert response.status_code == 201, response.text
    data = response.json()["data"]

    put_response = requests.put(
        data["signed_url"],
        data=image_bytes,
        headers={
            "Content-Type": "image/png",
            "x-amz-server-side-encryption": "aws:kms",
            "x-amz-server-side-encryption-aws-kms-key-id": data["kms_key_id"],
        },
        timeout=30,
    )
    assert put_response.status_code == 200

    return data


@pytest.mark.full_integration
class TestApiInitFile:
    def test_init01_creates_pending_record_without_public_url_and_uploads_to_s3(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)
        image_bytes = IMAGE_PATH.read_bytes()
        s3_client = get_s3_client()

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            data = _init_and_upload(client, headers, image_bytes, s3_client, name="init_test.png")

        file_id = data["file_id"]
        # bucket jest prywatny - juz nie budujemy/zwracamy golego, niepodpisanego URL
        assert data["url"] is None

        file_record = db_session.query(File).filter(File.id == file_id).first()
        assert file_record.status.value == "pending"
        assert file_record.user_id == user.id

        try:
            head = s3_client.head_object(Bucket=settings.s3_bucket_name, Key=file_record.s3_key)
            assert head["ContentLength"] == len(image_bytes)
        finally:
            s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=file_record.s3_key)

    def test_init02_invalid_payload_returns_422(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            response = client.post(
                "/files/init",
                json={
                    "name": "",
                    "original_name": "x",
                    "size": 0,
                    "mime_type": "x",
                    "file_type": "photo",
                    "catalog": "x",
                },
                headers=headers,
            )

        assert response.status_code == 422

    def test_init03_missing_auth_returns_401(self, db_session):
        client = make_client(db_session, *ROUTERS)

        response = client.post(
            "/files/init",
            json={
                "name": "x.png",
                "original_name": "x.png",
                "size": 1,
                "mime_type": "image/png",
                "file_type": "photo",
                "catalog": "tests",
            },
        )

        assert response.status_code == 401

    def test_init04_size_over_50mb_returns_422(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            response = client.post(
                "/files/init",
                json={
                    "name": "too_big.png",
                    "original_name": "too_big.png",
                    "size": 50 * 1024 * 1024 + 1,
                    "mime_type": "image/png",
                    "file_type": "photo",
                    "catalog": "tests",
                },
                headers=headers,
            )

        assert response.status_code == 422


@pytest.mark.full_integration
class TestApiUpdateFile:
    def test_update01_confirmed_status_moves_pending_to_completed(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)
        image_bytes = IMAGE_PATH.read_bytes()
        s3_client = get_s3_client()

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            init_data = _init_and_upload(client, headers, image_bytes, s3_client, name="update_status.png")
            file_id = init_data["file_id"]
            s3_key = db_session.query(File).filter(File.id == file_id).first().s3_key

            try:
                response = client.put(f"/files/update/{file_id}", json={"status": "confirmed"}, headers=headers)
                assert response.status_code == 200, response.text
                assert response.json()["data"]["status"] == "completed"
            finally:
                s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=s3_key)

    def test_update02_renames_file_without_touching_status(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)
        image_bytes = IMAGE_PATH.read_bytes()
        s3_client = get_s3_client()

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            init_data = _init_and_upload(client, headers, image_bytes, s3_client, name="do_zmiany.png")
            file_id = init_data["file_id"]
            s3_key = db_session.query(File).filter(File.id == file_id).first().s3_key

            try:
                response = client.put(f"/files/update/{file_id}", json={"name": "nowa_nazwa.png"}, headers=headers)
                assert response.status_code == 200, response.text
                data = response.json()["data"]
                assert data["name"] == "nowa_nazwa.png"
                assert data["status"] == "pending"
            finally:
                s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=s3_key)

    def test_update03_invalid_file_id_format_returns_400(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            response = client.put("/files/update/nie-uuid", json={"name": "x.png"}, headers=headers)

        assert response.status_code == 400

    def test_update04_not_found_returns_404(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            response = client.put(
                "/files/update/6fa459ea-ee8a-4ca4-894e-db77e160355e", json={"name": "x.png"}, headers=headers
            )

        assert response.status_code == 404


@pytest.mark.full_integration
class TestApiDeleteFile:
    def test_delete01_removes_db_record_and_real_s3_object(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)
        image_bytes = IMAGE_PATH.read_bytes()
        s3_client = get_s3_client()

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            init_data = _init_and_upload(client, headers, image_bytes, s3_client, name="do_usuniecia.png")
            file_id = init_data["file_id"]
            s3_key = db_session.query(File).filter(File.id == file_id).first().s3_key

            response = client.delete(f"/files/delete/{file_id}", headers=headers)

        assert response.status_code == 200, response.text
        assert response.json()["data"]["file_id"] == file_id
        assert db_session.query(File).filter(File.id == file_id).first() is None

        with pytest.raises(ClientError) as exc_info:
            s3_client.head_object(Bucket=settings.s3_bucket_name, Key=s3_key)
        assert exc_info.value.response["Error"]["Code"] == "404"

    def test_delete02_cascades_real_s3_objects_of_child_files(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)
        image_bytes = IMAGE_PATH.read_bytes()
        s3_client = get_s3_client()

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            parent_data = _init_and_upload(client, headers, image_bytes, s3_client, name="rodzic.png")
            child_data = _init_and_upload(client, headers, image_bytes, s3_client, name="dziecko.png")
            parent_id, child_id = parent_data["file_id"], child_data["file_id"]
            parent_key = db_session.query(File).filter(File.id == parent_id).first().s3_key
            child_key = db_session.query(File).filter(File.id == child_id).first().s3_key

            link_response = client.put(
                f"/files/metadata/{child_id}", json={"parent_file_id": parent_id}, headers=headers
            )
            assert link_response.status_code == 200, link_response.text

            delete_response = client.delete(f"/files/delete/{parent_id}", headers=headers)

        assert delete_response.status_code == 200, delete_response.text
        # CASCADE z bazy - dziecko znika razem z rodzicem
        assert db_session.query(File).filter(File.id.in_([parent_id, child_id])).count() == 0

        for key in (parent_key, child_key):
            with pytest.raises(ClientError) as exc_info:
                s3_client.head_object(Bucket=settings.s3_bucket_name, Key=key)
            assert exc_info.value.response["Error"]["Code"] == "404"

    def test_delete03_not_found_returns_404(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            response = client.delete(
                "/files/delete/6fa459ea-ee8a-4ca4-894e-db77e160355e", headers=headers
            )

        assert response.status_code == 404
