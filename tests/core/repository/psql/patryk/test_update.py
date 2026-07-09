from sqlalchemy.orm import Session

from core.repository.psql.patryk.update import update_calculator_keys_psql
from tests.core.repository.psql.patryk.helper import make_calculator_keys


class TestUpdateCalculatorKeysPsql:
    def test_update01_changes_all_values(self, db_session: Session):
        keys = make_calculator_keys(db_session)

        result, err, ok = update_calculator_keys_psql(
            str(keys.id), 0.19, 0.23, 13.5, 16.5, 20.5, 15.5, 10.5, 12.5, db_session=db_session
        )

        assert ok is True and err is None
        assert result.income_tax == 0.19
        assert result.inpost_parcel_locker == 13.5
        assert result.without_smart == 12.5

    def test_update02_missing_returns_not_found(self, db_session: Session):
        result, err, ok = update_calculator_keys_psql(
            "6fa459ea-ee8a-4ca4-894e-db77e160355e", 0.1, 0.2, 1, 2, 3, 4, 5, 6, db_session=db_session
        )

        assert ok is False and result is None
        assert err.key_type_error == "NotFound"
