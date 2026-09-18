"""Test API preview/download - realny S3, bez mockow poza JWT (full_integration)."""

from pathlib import Path
from uuid import uuid4

import pytest
import requests

from api.endpoints.file.download import router as download_router
from api.endpoints.file.init import router as init_router
from api.endpoints.file.preview import router as preview_router
from config.settings import settings
from core.infra.s3.config import get_s3_client
from database.psql.models.file import File, FileStatus
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.user.helper import create_test_user

ROUTERS = (init_router, preview_router, download_router)
IMAGE_PATH = Path(__file__).resolve().parents[3] / "files_for_tests" / "Patryk, fortnite,naruto.png"


def _upload_completed_file(client, headers, db_session, image_bytes: bytes, *, name: str) -> File:
    """Realny init + PUT na S3, potem status ustawiony bezposrednio na COMPLETED
    (bez przechodzenia przez PUT /files/update - to juz jest przetestowane osobno)."""
    response = client.post(
        "/files/init",
        json={
            "name": name,
            "original_name": name,
            "size": len(image_bytes),
            "mime_type": "image/png",
            "file_type": "photo",
            "catalog": "tests/api_preview_download",
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

    file_record = db_session.query(File).filter(File.id == data["file_id"]).first()
    file_record.status = FileStatus.COMPLETED
    db_session.flush()
    return file_record


@pytest.mark.full_integration
class TestApiPreviewFile:
    def test_preview01_returns_working_inline_presigned_url(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)
        image_bytes = IMAGE_PATH.read_bytes()
        s3_client = get_s3_client()

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            file_record = _upload_completed_file(client, headers, db_session, image_bytes, name="preview.png")

            try:
                response = client.get(f"/files/preview/{file_record.id}", headers=headers)
                assert response.status_code == 200, response.text
                data = response.json()["data"]
                assert data["expires_in_seconds"] == 180

                downloaded = requests.get(data["url"], timeout=30)
                assert downloaded.status_code == 200
                assert downloaded.content == image_bytes
                assert downloaded.headers["Content-Disposition"].startswith("inline")
            finally:
                s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=file_record.s3_key)

    def test_preview02_pending_file_returns_409(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            init_response = client.post(
                "/files/init",
                json={
                    "name": "still_pending.png",
                    "original_name": "still_pending.png",
                    "size": 10,
                    "mime_type": "image/png",
                    "file_type": "photo",
                    "catalog": "tests/api_preview_download",
                },
                headers=headers,
            )
            file_id = init_response.json()["data"]["file_id"]

            response = client.get(f"/files/preview/{file_id}", headers=headers)

        assert response.status_code == 409

    def test_preview03_not_found_returns_404(self, db_session):
        client = make_client(db_session, *ROUTERS)

        with authorized_as("superadmin") as headers:
            response = client.get(f"/files/preview/{uuid4()}", headers=headers)

        assert response.status_code == 404

    def test_preview04_invalid_uuid_returns_400(self, db_session):
        client = make_client(db_session, *ROUTERS)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/preview/not-a-uuid", headers=headers)

        assert response.status_code == 400


@pytest.mark.full_integration
class TestApiDownloadFile:
    def test_download01_redirects_to_working_attachment_presigned_url(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)
        image_bytes = IMAGE_PATH.read_bytes()
        s3_client = get_s3_client()

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            file_record = _upload_completed_file(client, headers, db_session, image_bytes, name="download.png")

            try:
                response = client.get(
                    f"/files/download/{file_record.id}", headers=headers, follow_redirects=False
                )
                assert response.status_code == 302
                signed_url = response.headers["location"]

                downloaded = requests.get(signed_url, timeout=30)
                assert downloaded.status_code == 200
                assert downloaded.content == image_bytes
                assert downloaded.headers["Content-Disposition"].startswith("attachment")
            finally:
                s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=file_record.s3_key)

    def test_download02_pending_file_returns_409(self, db_session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            init_response = client.post(
                "/files/init",
                json={
                    "name": "still_pending2.png",
                    "original_name": "still_pending2.png",
                    "size": 10,
                    "mime_type": "image/png",
                    "file_type": "photo",
                    "catalog": "tests/api_preview_download",
                },
                headers=headers,
            )
            file_id = init_response.json()["data"]["file_id"]

            response = client.get(f"/files/download/{file_id}", headers=headers, follow_redirects=False)

        assert response.status_code == 409

    def test_download03_not_found_returns_404(self, db_session):
        client = make_client(db_session, *ROUTERS)

        with authorized_as("superadmin") as headers:
            response = client.get(f"/files/download/{uuid4()}", headers=headers, follow_redirects=False)

        assert response.status_code == 404

    def test_download04_invalid_uuid_returns_400(self, db_session):
        client = make_client(db_session, *ROUTERS)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/download/not-a-uuid", headers=headers, follow_redirects=False)

        assert response.status_code == 400
