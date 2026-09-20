from uuid import uuid4

from sqlalchemy.orm import Session

from api.endpoints.file.node.collection import router as collection_router
from api.endpoints.file.node.create import router as create_router
from api.endpoints.file.node.delete import router as delete_router
from api.endpoints.file.node.one import router as one_router
from api.endpoints.file.node.update import router as update_router
from database.psql.models.file import FilesNode
from database.psql.models.logs import Logs
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.file.helper import make_file
from tests.core.repository.psql.file.node.helper import make_files_node
from tests.core.repository.psql.user.helper import create_test_user


class TestApiFilesNode:
    def test_node01_create_returns_201_and_saves_row(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post("/files/nodes/create", json={"name": "Mama"}, headers=headers)

        assert response.status_code == 201
        body = response.json()
        assert body["status"] == "SUCCESS"
        assert body["data"]["name"] == "Mama" and body["data"]["parent_id"] is None
        assert db_session.query(FilesNode).count() == 1

    def test_node02_create_with_parent_id(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca 2025-2026")
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/files/nodes/create", json={"name": "Faktura", "parent_id": str(parent.id)}, headers=headers
            )

        assert response.status_code == 201
        assert response.json()["data"]["parent_id"] == str(parent.id)

    def test_node03_create_duplicate_name_under_same_parent_returns_409(self, db_session: Session):
        # duplikat pod tym samym (realnym) rodzicem - dwa wezly najwyzszego poziomu
        # (parent_id=NULL) NIE naruszaja UniqueConstraint, bo NULL != NULL w Postgresie
        parent = make_files_node(db_session, name="Praca 2025-2026")
        make_files_node(db_session, name="Faktura", parent_id=str(parent.id))
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/files/nodes/create", json={"name": "Faktura", "parent_id": str(parent.id)}, headers=headers
            )

        assert response.status_code == 409

    def test_node04_create_empty_name_returns_422(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post("/files/nodes/create", json={"name": "   "}, headers=headers)

        assert response.status_code == 422

    def test_node05_collection_returns_top_level_by_default_and_filters_by_parent(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca 2025-2026")
        make_files_node(db_session, name="Faktura", parent_id=str(parent.id))
        make_files_node(db_session, name="Mama")
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            top_level = client.get("/files/nodes/collection", headers=headers)
            children = client.get("/files/nodes/collection", params={"parent_id": str(parent.id)}, headers=headers)

        assert {row["name"] for row in top_level.json()["data"]} == {"Praca 2025-2026", "Mama"}
        assert [row["name"] for row in children.json()["data"]] == ["Faktura"]

    def test_node06_collection_invalid_parent_id_returns_400(self, db_session: Session):
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/nodes/collection", params={"parent_id": "nie-uuid"}, headers=headers)

        assert response.status_code == 400

    def test_node07_one_returns_node_and_404_for_missing(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        client = make_client(db_session, one_router)

        with authorized_as("superadmin") as headers:
            found = client.get(f"/files/nodes/one/{node.id}", headers=headers)
            missing = client.get(f"/files/nodes/one/{uuid4()}", headers=headers)

        assert found.status_code == 200
        assert found.json()["data"]["node"]["name"] == "Mama"
        assert missing.status_code == 404

    def test_node07b_one_returns_breadcrumb_from_root_to_node(self, db_session: Session):
        root = make_files_node(db_session, name="Praca 2025-2026")
        middle = make_files_node(db_session, name="Faktury", parent_id=str(root.id))
        leaf = make_files_node(db_session, name="Faktura 3", parent_id=str(middle.id))
        client = make_client(db_session, one_router)

        with authorized_as("superadmin") as headers:
            response = client.get(f"/files/nodes/one/{leaf.id}", headers=headers)

        assert response.status_code == 200
        names = [item["name"] for item in response.json()["data"]["breadcrumb"]]
        assert names == ["Praca 2025-2026", "Faktury", "Faktura 3"]

    def test_node08_one_invalid_uuid_returns_400(self, db_session: Session):
        client = make_client(db_session, one_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/nodes/one/not-a-uuid", headers=headers)

        assert response.status_code == 400

    def test_node09_update_renames_and_changes_description(self, db_session: Session):
        node = make_files_node(db_session, name="Stara nazwa", description="stary opis")
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.put(
                f"/files/nodes/update/{node.id}",
                json={"name": "Nowa nazwa", "description": "nowy opis"},
                headers=headers,
            )

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["name"] == "Nowa nazwa" and data["description"] == "nowy opis"

    def test_node10_update_explicit_null_parent_id_moves_to_top_level(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca 2025-2026")
        child = make_files_node(db_session, name="Faktura", parent_id=str(parent.id))
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/nodes/update/{child.id}", json={"parent_id": None}, headers=headers)

        assert response.status_code == 200
        assert response.json()["data"]["parent_id"] is None

    def test_node11_update_omitted_parent_id_does_not_change_it(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca 2025-2026")
        child = make_files_node(db_session, name="Faktura", parent_id=str(parent.id))
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/nodes/update/{child.id}", json={"name": "Faktura 2"}, headers=headers)

        assert response.status_code == 200
        assert response.json()["data"]["parent_id"] == str(parent.id)

    def test_node12_update_not_found_returns_404(self, db_session: Session):
        client = make_client(db_session, update_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/nodes/update/{uuid4()}", json={"name": "x"}, headers=headers)

        assert response.status_code == 404

    def test_node13_delete_returns_200_and_removes_row(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete(f"/files/nodes/delete/{node.id}", headers=headers)

        assert response.status_code == 200
        assert db_session.query(FilesNode).count() == 0

    def test_node14_delete_with_child_node_returns_409(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca 2025-2026")
        make_files_node(db_session, name="Faktura", parent_id=str(parent.id))
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete(f"/files/nodes/delete/{parent.id}", headers=headers)

        assert response.status_code == 409

    def test_node15_delete_with_assigned_file_returns_409_with_clear_message(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        make_file(db_session, node_id=str(node.id))
        client = make_client(db_session, delete_router)

        with authorized_as("superadmin") as headers:
            response = client.delete(f"/files/nodes/delete/{node.id}", headers=headers)

        assert response.status_code == 409
        assert "przypisane pliki" in response.json()["data"]["message"]

    def test_node16_no_token_401_and_role_user_403(self, db_session: Session):
        client = make_client(db_session, create_router)

        no_token = client.post("/files/nodes/create", json={"name": "x"})
        with authorized_as("user") as headers:
            wrong_role = client.post("/files/nodes/create", json={"name": "x"}, headers=headers)

        assert no_token.status_code == 401
        assert wrong_role.status_code == 403

    def test_node17_create_writes_audit_log(self, db_session: Session):
        user = create_test_user(db_session, type="superadmin")
        client = make_client(db_session, create_router)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            client.post("/files/nodes/create", json={"name": "Audytowane"}, headers=headers)

        log = db_session.query(Logs).filter(Logs.description == "files:create_node").first()
        assert log is not None and log.username == user.username
