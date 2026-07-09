from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.patryk.response import KeysCalculatorResponse, _to_keys_calculator_response
from database.psql.database import managed_session
from database.psql.models.patryk import KeysCalculatorPatryk


def one_calculator_keys_psql(
    db_session: Session | None = None,
) -> tuple[KeysCalculatorResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            row_key = db.query(KeysCalculatorPatryk).first()
            if not row_key:
                return None, ApiErrorData(
                    message="Not found calculator keys",
                    type_module="one_calculator_keys_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            return _to_keys_calculator_response(row_key), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="one_calculator_keys_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
