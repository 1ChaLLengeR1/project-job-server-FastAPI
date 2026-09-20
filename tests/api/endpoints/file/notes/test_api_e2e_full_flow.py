"""Test e2e pełnego przepływu magazynu plików - realny S3 (full_integration).

Wszystko przez HTTP (TestClient), tak jak strzelałby frontend:
create wezel -> (per plik) init upload (presigned PUT) -> prawdziwy PUT bajtów
na S3 -> update statusu (`status=confirmed` -> wewnętrznie `completed`, zob.
`handler_update_file`) -> assign do węzła (-> status `confirmed`, `node_id`
ustawiony) -> próba usunięcia węzła z podpiętymi plikami (409, czytelny
komunikat - zob. `delete_files_node_psql`) -> delete każdego pliku pojedynczo
(rekord + prawdziwy obiekt S3) -> delete węzła (teraz bez plików, 200).
"""

from pathlib import Path

import pytest
import requests
from botocore.exceptions import ClientError
from sqlalchemy.orm import Session

from api.endpoints.file.assign import router as file_assign_router
from api.endpoints.file.delete import router as file_delete_router
from api.endpoints.file.init import router as file_init_router
from api.endpoints.file.node.create import router as node_create_router
from api.endpoints.file.node.delete import router as node_delete_router
from api.endpoints.file.update import router as file_update_router
from config.settings import settings
from core.infra.s3.config import get_s3_client
from database.psql.models.file import File, FileType
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.user.helper import create_test_user

ROUTERS = (
    node_create_router,
    node_delete_router,
    file_init_router,
    file_update_router,
    file_assign_router,
    file_delete_router,
)

IMAGE_PATH = Path(__file__).resolve().parents[4] / "files_for_tests" / "Patryk, fortnite,naruto.png"
FILES_COUNT = 3


@pytest.mark.full_integration
class TestApiE2EFullFileNodesFlow:
    def _post(self, client, headers, url, payload):
        response = client.post(url, json=payload, headers=headers)
        assert response.status_code == 201, f"{url}: {response.text}"
        return response.json()["data"]

    def test_e2e01_create_node_upload_assign_then_delete_files_then_node(self, db_session: Session):
        client = make_client(db_session, *ROUTERS)
        user = create_test_user(db_session)
        image_bytes = IMAGE_PATH.read_bytes()
        s3_client = get_s3_client()
        s3_keys: list[str] = []

        try:
            with authorized_as("superadmin", user_id=str(user.id)) as headers:
                # 1. wezel (osoba/kategoria), po ktorym rozpinamy pliki
                node = self._post(client, headers, "/files/nodes/create", {"name": "E2E testowy węzeł"})
                node_id = node["id"]

                # 2. per plik: init (presigned PUT) -> prawdziwy upload na S3 -> potwierdzenie
                #    zakonczenia (completed) -> assign do wezla (confirmed)
                file_ids: list[str] = []
                for i in range(FILES_COUNT):
                    init_data = self._post(
                        client,
                        headers,
                        "/files/init",
                        {
                            "name": f"e2e_{i}.png",
                            "original_name": f"zdjecie_{i}.png",
                            "size": len(image_bytes),
                            "mime_type": "image/png",
                            "file_type": FileType.PHOTO.value,
                            "catalog": "tests/e2e_files_nodes",
                        },
                    )
                    file_id = init_data["file_id"]
                    file_ids.append(file_id)

                    # zapamietujemy s3_key od razu - bezpiecznik w finally musi je znac
                    # nawet jesli test wybuchnie pozniej, przed dojsciem do delete
                    file_record = db_session.query(File).filter(File.id == file_id).first()
                    s3_keys.append(file_record.s3_key)

                    put_response = requests.put(
                        init_data["signed_url"],
                        data=image_bytes,
                        headers={
                            "Content-Type": "image/png",
                            "x-amz-server-side-encryption": "aws:kms",
                            "x-amz-server-side-encryption-aws-kms-key-id": init_data["kms_key_id"],
                        },
                        timeout=30,
                    )
                    assert put_response.status_code == 200

                    update_resp = client.put(f"/files/update/{file_id}", json={"status": "confirmed"}, headers=headers)
                    assert update_resp.status_code == 200, update_resp.text
                    assert update_resp.json()["data"]["status"] == "completed"

                    assign_resp = client.put(f"/files/assign/{file_id}", json={"node_id": node_id}, headers=headers)
                    assert assign_resp.status_code == 200, assign_resp.text
                    assign_data = assign_resp.json()["data"]
                    assert assign_data["status"] == "confirmed"
                    assert assign_data["node_id"] == node_id

                # 3. wezel ma podpiete pliki - usuniecie musi byc zablokowane, czytelny komunikat
                blocked = client.delete(f"/files/nodes/delete/{node_id}", headers=headers)
                assert blocked.status_code == 409, blocked.text
                assert "przypisane pliki" in blocked.json()["data"]["message"]

                # 4. usuniecie kazdego pliku pojedynczo - rekord w bazie + realny obiekt S3
                for file_id, s3_key in zip(file_ids, s3_keys, strict=True):
                    delete_resp = client.delete(f"/files/delete/{file_id}", headers=headers)
                    assert delete_resp.status_code == 200, delete_resp.text
                    assert delete_resp.json()["data"]["file_id"] == file_id

                    with pytest.raises(ClientError) as exc_info:
                        s3_client.head_object(Bucket=settings.s3_bucket_name, Key=s3_key)
                    assert exc_info.value.response["Error"]["Code"] == "404"

                # 5. wezel bez plikow - usuniecie teraz przechodzi
                final_delete = client.delete(f"/files/nodes/delete/{node_id}", headers=headers)
                assert final_delete.status_code == 200, final_delete.text
        finally:
            # bezpiecznik - gdyby asercja wybuchla przed dojsciem do delete, sprzatamy
            # realne obiekty S3 niezaleznie od wyniku testu
            for key in s3_keys:
                s3_client.delete_object(Bucket=settings.s3_bucket_name, Key=key)
