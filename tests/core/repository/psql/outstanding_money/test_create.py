from sqlalchemy.orm import Session

from core.repository.psql.outstanding_money.create import add_item_psql, create_list_psql
from tests.core.repository.psql.outstanding_money.helper import make_overdue_list

MISSING_UUID = "6fa459ea-ee8a-4ca4-894e-db77e160355e"


class TestCreateListPsql:
    def test_create_list01_creates_list_with_items(self, db_session: Session):
        items = [{"amount": 100.5, "name": "faktura 1"}, {"amount": 50.0, "name": "faktura 2"}]

        result, err, ok = create_list_psql("moja lista", items, db_session=db_session)

        assert ok is True and err is None
        assert result.names_overdue.name == "moja lista"
        assert len(result.new_outstanding_money) == 2
        assert all(item.id for item in result.new_outstanding_money)
        assert all(item.id_name == result.names_overdue.id for item in result.new_outstanding_money)

    def test_create_list02_empty_items_creates_empty_list(self, db_session: Session):
        result, err, ok = create_list_psql("pusta lista", [], db_session=db_session)

        assert ok is True
        assert result.new_outstanding_money == []


class TestAddItemPsql:
    def test_add_item01_appends_to_existing_list(self, db_session: Session):
        overdue = make_overdue_list(db_session)

        result, err, ok = add_item_psql(str(overdue.id), 25.0, "nowa pozycja", db_session=db_session)

        assert ok is True and err is None
        assert result.amount == 25.0
        assert result.name == "nowa pozycja"
        assert result.id_name == str(overdue.id)

    def test_add_item02_missing_list_returns_not_found(self, db_session: Session):
        result, err, ok = add_item_psql(MISSING_UUID, 25.0, "x", db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
