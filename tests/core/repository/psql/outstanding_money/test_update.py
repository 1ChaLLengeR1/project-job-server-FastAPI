from sqlalchemy.orm import Session

from core.repository.psql.outstanding_money.update import edit_item_psql, edit_name_list_psql
from tests.core.repository.psql.outstanding_money.helper import make_item, make_overdue_list

MISSING_UUID = "6fa459ea-ee8a-4ca4-894e-db77e160355e"


class TestEditNameListPsql:
    def test_edit_name01_changes_list_name(self, db_session: Session):
        overdue = make_overdue_list(db_session, name="stara nazwa")

        result, err, ok = edit_name_list_psql(str(overdue.id), "nowa nazwa", db_session=db_session)

        assert ok is True and err is None
        assert result.name == "nowa nazwa"

    def test_edit_name02_missing_list_returns_not_found(self, db_session: Session):
        result, err, ok = edit_name_list_psql(MISSING_UUID, "x", db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"


class TestEditItemPsql:
    def test_edit_item01_changes_amount_and_name(self, db_session: Session):
        overdue = make_overdue_list(db_session)
        item = make_item(db_session, id_name=overdue.id, amount=10)

        result, err, ok = edit_item_psql(str(item.id), 99.9, "poprawiona", db_session=db_session)

        assert ok is True and err is None
        assert result.amount == 99.9
        assert result.name == "poprawiona"

    def test_edit_item02_missing_item_returns_not_found(self, db_session: Session):
        result, err, ok = edit_item_psql(MISSING_UUID, 1, "x", db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
