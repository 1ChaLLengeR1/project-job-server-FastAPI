from datetime import date, datetime, timedelta, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from api.endpoints.file.collection import router as collection_router
from api.endpoints.file.guarantees import router as guarantees_router
from api.endpoints.file.one import router as one_router
from api.endpoints.file.unassigned import router as unassigned_router
from database.psql.models.file import FileStatus, FileType
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.file.helper import make_file
from tests.core.repository.psql.file.node.helper import make_files_node


class TestApiCollectionFiles:
    def test_collection01_filters_by_file_type(self, db_session: Session):
        make_file(db_session, name="a.png", file_type=FileType.PHOTO)
        make_file(db_session, name="b.mp4", file_type=FileType.VIDEO)
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/collection", params={"file_type": "video"}, headers=headers)

        assert response.status_code == 200
        assert [row["name"] for row in response.json()["data"]["data"]] == ["b.mp4"]

    def test_collection02_filters_by_node_id_recursive(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca")
        child_node = make_files_node(db_session, name="2026", parent_id=str(parent.id))
        make_file(db_session, name="wprost.png", node_id=str(parent.id))
        make_file(db_session, name="dziecko.png", node_id=str(child_node.id))
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            non_recursive = client.get(
                "/files/collection", params={"node_id": str(parent.id)}, headers=headers
            )
            recursive = client.get(
                "/files/collection", params={"node_id": str(parent.id), "recursive": True}, headers=headers
            )

        assert {r["name"] for r in non_recursive.json()["data"]["data"]} == {"wprost.png"}
        assert {r["name"] for r in recursive.json()["data"]["data"]} == {"wprost.png", "dziecko.png"}

    def test_collection03_invalid_node_id_returns_400(self, db_session: Session):
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/collection", params={"node_id": "nie-uuid"}, headers=headers)

        assert response.status_code == 400

    def test_collection04_filters_by_created_at_range(self, db_session: Session):
        old_file = make_file(db_session, name="stary.png")
        old_file.created_at = datetime(2020, 1, 1, tzinfo=timezone.utc)
        new_file = make_file(db_session, name="nowy.png")
        new_file.created_at = datetime(2026, 6, 15, 12, 0, tzinfo=timezone.utc)
        db_session.flush()
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get(
                "/files/collection",
                params={"created_at_from": "2026-01-01", "created_at_to": "2026-12-31"},
                headers=headers,
            )

        assert [row["name"] for row in response.json()["data"]["data"]] == ["nowy.png"]

    def test_collection05_filters_by_guarantee_status(self, db_session: Session):
        today = date.today()
        make_file(db_session, name="aktywna.png", guarantee_end_date=today + timedelta(days=10))
        make_file(db_session, name="wygasla.png", guarantee_end_date=today - timedelta(days=1))
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/collection", params={"guarantee_status": "active"}, headers=headers)

        assert [row["name"] for row in response.json()["data"]["data"]] == ["aktywna.png"]

    def test_collection06_pagination_fields_present(self, db_session: Session):
        for i in range(3):
            make_file(db_session, name=f"plik_{i}.png")
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/collection", params={"limit": 2}, headers=headers)

        pagination = response.json()["data"]["pagination"]
        assert pagination["total"] == 3 and pagination["limit"] == 2 and pagination["has_more"] is True


class TestApiOneFile:
    def test_one01_returns_file_with_direct_children(self, db_session: Session):
        parent = make_file(db_session, original_name="faktura.png")
        child = make_file(db_session, original_name="faktura-1.png", parent_file_id=str(parent.id))
        client = make_client(db_session, one_router)

        with authorized_as("superadmin") as headers:
            response = client.get(f"/files/one/{parent.id}", headers=headers)

        assert response.status_code == 200
        body = response.json()["data"]
        assert body["file"]["id"] == str(parent.id)
        assert [c["id"] for c in body["children"]] == [str(child.id)]

    def test_one02_not_found_returns_404(self, db_session: Session):
        client = make_client(db_session, one_router)

        with authorized_as("superadmin") as headers:
            response = client.get(f"/files/one/{uuid4()}", headers=headers)

        assert response.status_code == 404

    def test_one03_invalid_uuid_returns_400(self, db_session: Session):
        client = make_client(db_session, one_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/one/not-a-uuid", headers=headers)

        assert response.status_code == 400


class TestApiUnassignedFiles:
    def test_unassigned01_returns_only_completed_without_node(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        make_file(db_session, name="osierocony.png", status=FileStatus.COMPLETED)
        make_file(db_session, name="przypisany.png", status=FileStatus.CONFIRMED, node_id=str(node.id))
        make_file(db_session, name="pending.png", status=FileStatus.PENDING)
        client = make_client(db_session, unassigned_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/unassigned", headers=headers)

        assert response.status_code == 200
        assert [row["name"] for row in response.json()["data"]["data"]] == ["osierocony.png"]

    def test_unassigned02_empty_when_nothing_matches(self, db_session: Session):
        make_file(db_session, status=FileStatus.PENDING)
        client = make_client(db_session, unassigned_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/unassigned", headers=headers)

        assert response.json()["data"]["data"] == []


class TestApiExpiringGuarantees:
    def test_expiring01_returns_sorted_within_30_days(self, db_session: Session):
        today = date.today()
        make_file(db_session, name="za_5_dni.png", guarantee_end_date=today + timedelta(days=5))
        make_file(db_session, name="za_1_dzien.png", guarantee_end_date=today + timedelta(days=1))
        make_file(db_session, name="za_31_dni.png", guarantee_end_date=today + timedelta(days=31))
        make_file(db_session, name="wygasla.png", guarantee_end_date=today - timedelta(days=1))
        client = make_client(db_session, guarantees_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/guarantees/expiring", headers=headers)

        assert [row["name"] for row in response.json()["data"]["data"]] == ["za_1_dzien.png", "za_5_dni.png"]

    def test_expiring02_empty_when_nothing_expiring_soon(self, db_session: Session):
        make_file(db_session, guarantee_end_date=date.today() + timedelta(days=90))
        client = make_client(db_session, guarantees_router)

        with authorized_as("superadmin") as headers:
            response = client.get("/files/guarantees/expiring", headers=headers)

        assert response.json()["data"]["data"] == []
