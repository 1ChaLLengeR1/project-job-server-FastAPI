from datetime import date, timedelta

from sqlalchemy.orm import Session

from core.repository.psql.file.guarantees import collection_expiring_guarantees_psql
from tests.core.repository.psql.file.helper import make_file


class TestCollectionExpiringGuaranteesPsql:
    def test_expiring01_returns_only_within_next_30_days_sorted_ascending(self, db_session: Session):
        today = date.today()
        soon = make_file(db_session, name="za_5_dni.png", guarantee_end_date=today + timedelta(days=5))
        soonest = make_file(db_session, name="za_1_dzien.png", guarantee_end_date=today + timedelta(days=1))
        make_file(db_session, name="za_31_dni.png", guarantee_end_date=today + timedelta(days=31))
        make_file(db_session, name="wygasla.png", guarantee_end_date=today - timedelta(days=1))
        make_file(db_session, name="bez_gwarancji.png")

        result, err, ok = collection_expiring_guarantees_psql(db_session=db_session)

        assert ok is True and err is None
        assert [f.name for f in result.data] == ["za_1_dzien.png", "za_5_dni.png"]
        assert [f.id for f in result.data] == [str(soonest.id), str(soon.id)]

    def test_expiring02_boundary_today_and_30_days_are_included(self, db_session: Session):
        today = date.today()
        make_file(db_session, name="dzis.png", guarantee_end_date=today)
        make_file(db_session, name="za_30_dni.png", guarantee_end_date=today + timedelta(days=30))
        make_file(db_session, name="za_31_dni.png", guarantee_end_date=today + timedelta(days=31))

        result, err, ok = collection_expiring_guarantees_psql(db_session=db_session)

        assert ok is True
        assert {f.name for f in result.data} == {"dzis.png", "za_30_dni.png"}

    def test_expiring03_empty_when_nothing_expiring_soon(self, db_session: Session):
        make_file(db_session, name="daleka.png", guarantee_end_date=date.today() + timedelta(days=90))

        result, err, ok = collection_expiring_guarantees_psql(db_session=db_session)

        assert ok is True
        assert result.data == []
