from sqlalchemy.orm import Session

from core.repository.psql.patryk.one import one_calculator_keys_psql
from tests.core.repository.psql.patryk.helper import make_calculator_keys


class TestOneCalculatorKeysPsql:
    def test_one01_returns_keys(self, db_session: Session):
        keys = make_calculator_keys(db_session, vat=0.23, income_tax=0.12)

        result, err, ok = one_calculator_keys_psql(db_session=db_session)

        assert ok is True and err is None
        assert result.id == str(keys.id)
        assert result.vat == 0.23
        assert result.income_tax == 0.12

    def test_one02_empty_table_returns_not_found(self, db_session: Session):
        result, err, ok = one_calculator_keys_psql(db_session=db_session)

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
        assert err.type_module == "one_calculator_keys_psql"
