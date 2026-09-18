from datetime import date, datetime, timedelta, timezone

from sqlalchemy.orm import Session

from core.repository.psql.file.collection import collection_files_psql
from database.psql.models.file import FileStatus
from tests.core.repository.psql.file.helper import make_file
from tests.core.repository.psql.file.node.helper import make_files_node


class TestCollectionFilesPsql:
    def test_collection01_filters_by_exact_node_id(self, db_session: Session):
        node_a = make_files_node(db_session, name="A")
        node_b = make_files_node(db_session, name="B")
        make_file(db_session, name="a.png", node_id=str(node_a.id))
        make_file(db_session, name="b.png", node_id=str(node_b.id))
        make_file(db_session, name="bez_wezla.png")

        result, err, ok = collection_files_psql(node_id=str(node_a.id), db_session=db_session)

        assert ok is True and err is None
        assert [file.name for file in result.data] == ["a.png"]

    def test_collection02_recursive_includes_files_from_child_nodes(self, db_session: Session):
        parent = make_files_node(db_session, name="Praca")
        child_node = make_files_node(db_session, name="2026", parent_id=str(parent.id))
        make_file(db_session, name="wprost_pod_parent.png", node_id=str(parent.id))
        make_file(db_session, name="pod_dzieckiem.png", node_id=str(child_node.id))

        non_recursive, _, _ = collection_files_psql(node_id=str(parent.id), db_session=db_session)
        recursive, _, _ = collection_files_psql(node_id=str(parent.id), recursive=True, db_session=db_session)

        assert {file.name for file in non_recursive.data} == {"wprost_pod_parent.png"}
        assert {file.name for file in recursive.data} == {"wprost_pod_parent.png", "pod_dzieckiem.png"}

    def test_collection03_filters_by_created_at_range(self, db_session: Session):
        old_file = make_file(db_session, name="stary.png")
        old_file.created_at = datetime(2020, 1, 1, tzinfo=timezone.utc)
        new_file = make_file(db_session, name="nowy.png")
        new_file.created_at = datetime(2026, 6, 15, tzinfo=timezone.utc)
        db_session.flush()

        result, err, ok = collection_files_psql(
            created_at_from=date(2026, 1, 1), created_at_to=date(2026, 12, 31), db_session=db_session
        )

        assert ok is True
        assert [file.name for file in result.data] == ["nowy.png"]

    def test_collection04_created_at_to_is_inclusive_of_whole_day(self, db_session: Session):
        # 20:30 UTC = 22:30 czasu Warszawy (DB ma `timezone=Europe/Warsaw") - bezpiecznie
        # w środku 15.06, nie koło północy, żeby uniknąć przesunięcia na inny dzień
        same_day_file = make_file(db_session, name="tego_samego_dnia.png")
        same_day_file.created_at = datetime(2026, 6, 15, 20, 30, tzinfo=timezone.utc)
        db_session.flush()

        result, err, ok = collection_files_psql(created_at_to=date(2026, 6, 15), db_session=db_session)

        assert ok is True
        assert [file.name for file in result.data] == ["tego_samego_dnia.png"]

    def test_collection05_empty_when_node_has_no_files(self, db_session: Session):
        node = make_files_node(db_session, name="Pusty")
        make_file(db_session, name="inny.png", status=FileStatus.COMPLETED)

        result, err, ok = collection_files_psql(node_id=str(node.id), db_session=db_session)

        assert ok is True
        assert result.data == []

    def test_collection06_guarantee_status_active_expired_none(self, db_session: Session):
        today = date.today()
        make_file(db_session, name="aktywna.png", guarantee_end_date=today + timedelta(days=10))
        make_file(db_session, name="wygasla.png", guarantee_end_date=today - timedelta(days=1))
        make_file(db_session, name="bez_gwarancji.png")
        make_file(db_session, name="tylko_start.png", guarantee_start_date=today - timedelta(days=5))

        active, _, _ = collection_files_psql(guarantee_status="active", db_session=db_session)
        expired, _, _ = collection_files_psql(guarantee_status="expired", db_session=db_session)
        none, _, _ = collection_files_psql(guarantee_status="none", db_session=db_session)

        assert [f.name for f in active.data] == ["aktywna.png"]
        assert [f.name for f in expired.data] == ["wygasla.png"]
        # "tylko_start" ma start_date, ale bez end_date liczy sie jako "none" (ustalone z uzytkownikiem)
        assert {f.name for f in none.data} == {"bez_gwarancji.png", "tylko_start.png"}

    def test_collection07_guarantee_active_includes_end_date_today(self, db_session: Session):
        make_file(db_session, name="dzis.png", guarantee_end_date=date.today())

        active, _, _ = collection_files_psql(guarantee_status="active", db_session=db_session)

        assert [f.name for f in active.data] == ["dzis.png"]

    def test_collection08_filters_by_status(self, db_session: Session):
        node = make_files_node(db_session, name="Mama")
        make_file(db_session, name="pending.png", status=FileStatus.PENDING)
        make_file(db_session, name="completed.png", status=FileStatus.COMPLETED)
        make_file(db_session, name="confirmed.png", status=FileStatus.CONFIRMED, node_id=str(node.id))

        completed, _, _ = collection_files_psql(status="completed", db_session=db_session)
        confirmed, _, _ = collection_files_psql(status="confirmed", db_session=db_session)
        without_filter, _, _ = collection_files_psql(db_session=db_session)

        assert [f.name for f in completed.data] == ["completed.png"]
        assert [f.name for f in confirmed.data] == ["confirmed.png"]
        assert {f.name for f in without_filter.data} == {"pending.png", "completed.png", "confirmed.png"}
