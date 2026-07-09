from sqlalchemy.orm import Session

from core.repository.psql.outstanding_money.collection import collection_list_psql
from tests.core.repository.psql.outstanding_money.helper import make_item, make_overdue_list


class TestCollectionListPsql:
    def test_collection01_aggregates_items_and_full_price(self, db_session: Session):
        overdue = make_overdue_list(db_session, name="lista A")
        make_item(db_session, id_name=overdue.id, amount=100.5)
        make_item(db_session, id_name=overdue.id, amount=50.0)

        result, err, ok = collection_list_psql(db_session=db_session)

        assert ok is True and err is None
        assert len(result) == 1
        assert result[0].name_overdue == "lista A"
        assert len(result[0].array_items) == 2
        assert result[0].full_price == 150.5

    def test_collection02_list_without_items_has_zero_price(self, db_session: Session):
        make_overdue_list(db_session)

        result, err, ok = collection_list_psql(db_session=db_session)

        assert ok is True
        assert result[0].array_items == [] and result[0].full_price == 0

    def test_collection03_empty_returns_empty_list(self, db_session: Session):
        result, err, ok = collection_list_psql(db_session=db_session)

        assert ok is True and result == []
