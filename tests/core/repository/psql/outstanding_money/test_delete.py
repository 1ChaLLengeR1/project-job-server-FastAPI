from sqlalchemy.orm import Session

from core.repository.psql.outstanding_money.delete import delete_item_psql, delete_list_psql
from database.psql.models.outstanding_money import NamesOverdue, OutStandingMoney
from tests.core.repository.psql.outstanding_money.helper import make_item, make_overdue_list

MISSING_UUID = "6fa459ea-ee8a-4ca4-894e-db77e160355e"


class TestDeleteListPsql:
    def test_delete_list01_removes_list_with_items(self, db_session: Session):
        overdue = make_overdue_list(db_session)
        make_item(db_session, id_name=overdue.id)
        make_item(db_session, id_name=overdue.id)

        result, err, ok = delete_list_psql(str(overdue.id), db_session=db_session)

        assert ok is True and err is None
        assert len(result.outstanding_money) == 2
        assert db_session.query(NamesOverdue).count() == 0
        assert db_session.query(OutStandingMoney).count() == 0

    def test_delete_list02_empty_list_is_deletable(self, db_session: Session):
        overdue = make_overdue_list(db_session)

        result, err, ok = delete_list_psql(str(overdue.id), db_session=db_session)

        assert ok is True
        assert result.outstanding_money == []
        assert db_session.query(NamesOverdue).count() == 0

    def test_delete_list03_missing_returns_not_found(self, db_session: Session):
        result, err, ok = delete_list_psql(MISSING_UUID, db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"


class TestDeleteItemPsql:
    def test_delete_item01_removes_single_item(self, db_session: Session):
        overdue = make_overdue_list(db_session)
        item = make_item(db_session, id_name=overdue.id, amount=42)

        result, err, ok = delete_item_psql(str(item.id), db_session=db_session)

        assert ok is True and err is None
        assert result.amount == 42
        assert db_session.query(OutStandingMoney).count() == 0
        assert db_session.query(NamesOverdue).count() == 1  # lista zostaje

    def test_delete_item02_missing_returns_not_found(self, db_session: Session):
        result, err, ok = delete_item_psql(MISSING_UUID, db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
