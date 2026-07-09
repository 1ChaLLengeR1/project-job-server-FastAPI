from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.patryk.response import KeysCalculatorResponse
from core.repository.psql.patryk.update import update_calculator_keys_psql


def handler_update_calculator_keys(
    user_id: str,
    keys_id: str,
    income_tax: float,
    vat: float,
    inpost_parcel_locker: float,
    inpost_courier: float,
    inpost_cash_of_delivery_courier: float,
    dpd: float,
    allegro_matt: float,
    without_smart: float,
    db_session: Session | None = None,
) -> tuple[KeysCalculatorResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_calculator_keys_psql(
            keys_id,
            income_tax,
            vat,
            inpost_parcel_locker,
            inpost_courier,
            inpost_cash_of_delivery_courier,
            dpd,
            allegro_matt,
            without_smart,
            db_session=db_session,
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "calculator_work:update", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_update_calculator_keys",
            type_error="exception",
            key_type_error="Exception",
        ), False
