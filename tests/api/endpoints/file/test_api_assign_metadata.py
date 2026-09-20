from uuid import uuid4

from sqlalchemy.orm import Session

from api.endpoints.file.assign import router as assign_router
from api.endpoints.file.metadata import router as metadata_router
from api.endpoints.file.unassigned import router as unassigned_router
from database.psql.models.file import FileStatus
from database.psql.models.logs import Logs
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.file.helper import make_file
from tests.core.repository.psql.file.node.helper import make_files_node
from tests.core.repository.psql.user.helper import create_test_user


class TestApiAssignFile:
    def test_assign01_completed_file_becomes_confirmed_with_node(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        file = make_file(db_session, status=FileStatus.COMPLETED)
        client = make_client(db_session, assign_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/assign/{file.id}", json={"node_id": str(node.id)}, headers=headers)

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["status"] == "confirmed" and data["node_id"] == str(node.id)

    def test_assign02_with_parent_file_id(self, db_session: Session):
        node = make_files_node(db_session, name="Praca 2025-2026")
        parent_file = make_file(db_session, status=FileStatus.CONFIRMED, node_id=str(node.id))
        file = make_file(db_session, status=FileStatus.COMPLETED)
        client = make_client(db_session, assign_router)

        with authorized_as("superadmin") as headers:
            response = client.put(
                f"/files/assign/{file.id}",
                json={"node_id": str(node.id), "parent_file_id": str(parent_file.id)},
                headers=headers,
            )

        assert response.status_code == 200
        assert response.json()["data"]["parent_file_id"] == str(parent_file.id)

    def test_assign03_wrong_status_returns_409(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        file = make_file(db_session, status=FileStatus.PENDING)
        client = make_client(db_session, assign_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/assign/{file.id}", json={"node_id": str(node.id)}, headers=headers)

        assert response.status_code == 409

    def test_assign04_invalid_file_id_format_returns_400(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        client = make_client(db_session, assign_router)

        with authorized_as("superadmin") as headers:
            response = client.put("/files/assign/nie-uuid", json={"node_id": str(node.id)}, headers=headers)

        assert response.status_code == 400

    def test_assign05_not_found_returns_404(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        client = make_client(db_session, assign_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/assign/{uuid4()}", json={"node_id": str(node.id)}, headers=headers)

        assert response.status_code == 404

    def test_assign06_invalid_node_id_in_body_returns_422(self, db_session: Session):
        file = make_file(db_session, status=FileStatus.COMPLETED)
        client = make_client(db_session, assign_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/assign/{file.id}", json={"node_id": "nie-uuid"}, headers=headers)

        assert response.status_code == 422

    def test_assign07_writes_audit_log(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        file = make_file(db_session, status=FileStatus.COMPLETED)
        user = create_test_user(db_session, type="superadmin")
        client = make_client(db_session, assign_router)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            client.put(f"/files/assign/{file.id}", json={"node_id": str(node.id)}, headers=headers)

        log = db_session.query(Logs).filter(Logs.description == "files:assign").first()
        assert log is not None and log.username == user.username


class TestApiUnassignFile:
    def test_unassign01_confirmed_file_becomes_completed_without_node(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        file = make_file(db_session, status=FileStatus.CONFIRMED, node_id=str(node.id))
        client = make_client(db_session, unassigned_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/unassign/{file.id}", headers=headers)

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["status"] == "completed" and data["node_id"] is None

    def test_unassign02_wrong_status_returns_409(self, db_session: Session):
        file = make_file(db_session, status=FileStatus.COMPLETED)
        client = make_client(db_session, unassigned_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/unassign/{file.id}", headers=headers)

        assert response.status_code == 409

    def test_unassign03_invalid_file_id_format_returns_400(self, db_session: Session):
        client = make_client(db_session, unassigned_router)

        with authorized_as("superadmin") as headers:
            response = client.put("/files/unassign/nie-uuid", headers=headers)

        assert response.status_code == 400

    def test_unassign04_not_found_returns_404(self, db_session: Session):
        client = make_client(db_session, unassigned_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/unassign/{uuid4()}", headers=headers)

        assert response.status_code == 404

    def test_unassign05_writes_audit_log(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        file = make_file(db_session, status=FileStatus.CONFIRMED, node_id=str(node.id))
        user = create_test_user(db_session, type="superadmin")
        client = make_client(db_session, unassigned_router)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            client.put(f"/files/unassign/{file.id}", headers=headers)

        log = db_session.query(Logs).filter(Logs.description == "files:unassign").first()
        assert log is not None and log.username == user.username


class TestApiUpdateFileMetadata:
    def test_metadata01_renames_original_name(self, db_session: Session):
        file = make_file(db_session, original_name="stara.png")
        client = make_client(db_session, metadata_router)

        with authorized_as("superadmin") as headers:
            response = client.put(
                f"/files/metadata/{file.id}", json={"original_name": "nowa.png"}, headers=headers
            )

        assert response.status_code == 200
        assert response.json()["data"]["original_name"] == "nowa.png"

    def test_metadata02_moves_file_to_different_node(self, db_session: Session):
        old_node = make_files_node(db_session, name="Mama")
        new_node = make_files_node(db_session, name="Ja")
        file = make_file(db_session, status=FileStatus.CONFIRMED, node_id=str(old_node.id))
        client = make_client(db_session, metadata_router)

        with authorized_as("superadmin") as headers:
            response = client.put(
                f"/files/metadata/{file.id}", json={"node_id": str(new_node.id)}, headers=headers
            )

        assert response.status_code == 200
        assert response.json()["data"]["node_id"] == str(new_node.id)

    def test_metadata03_explicit_null_parent_file_id_clears_it(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        parent_file = make_file(db_session, status=FileStatus.CONFIRMED, node_id=str(node.id))
        file = make_file(
            db_session, status=FileStatus.CONFIRMED, node_id=str(node.id), parent_file_id=str(parent_file.id)
        )
        client = make_client(db_session, metadata_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/metadata/{file.id}", json={"parent_file_id": None}, headers=headers)

        assert response.status_code == 200
        assert response.json()["data"]["parent_file_id"] is None

    def test_metadata04_omitted_parent_file_id_does_not_change_it(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        parent_file = make_file(db_session, status=FileStatus.CONFIRMED, node_id=str(node.id))
        file = make_file(
            db_session, status=FileStatus.CONFIRMED, node_id=str(node.id), parent_file_id=str(parent_file.id)
        )
        client = make_client(db_session, metadata_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/metadata/{file.id}", json={"description": "opis"}, headers=headers)

        assert response.status_code == 200
        assert response.json()["data"]["parent_file_id"] == str(parent_file.id)

    def test_metadata05_sets_description_and_guarantee_dates(self, db_session: Session):
        file = make_file(db_session)
        client = make_client(db_session, metadata_router)

        with authorized_as("superadmin") as headers:
            response = client.put(
                f"/files/metadata/{file.id}",
                json={
                    "description": "faktura AGD",
                    "guarantee_start_date": "2026-01-01",
                    "guarantee_end_date": "2028-01-01",
                },
                headers=headers,
            )

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["description"] == "faktura AGD"
        assert data["guarantee_start_date"] == "2026-01-01"
        assert data["guarantee_end_date"] == "2028-01-01"

    def test_metadata06_invalid_file_id_format_returns_400(self, db_session: Session):
        client = make_client(db_session, metadata_router)

        with authorized_as("superadmin") as headers:
            response = client.put("/files/metadata/nie-uuid", json={"description": "x"}, headers=headers)

        assert response.status_code == 400

    def test_metadata07_not_found_returns_404(self, db_session: Session):
        client = make_client(db_session, metadata_router)

        with authorized_as("superadmin") as headers:
            response = client.put(f"/files/metadata/{uuid4()}", json={"description": "x"}, headers=headers)

        assert response.status_code == 404

    def test_metadata08_writes_audit_log(self, db_session: Session):
        file = make_file(db_session)
        user = create_test_user(db_session, type="superadmin")
        client = make_client(db_session, metadata_router)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            client.put(f"/files/metadata/{file.id}", json={"description": "x"}, headers=headers)

        log = db_session.query(Logs).filter(Logs.description == "files:update_metadata").first()
        assert log is not None and log.username == user.username
