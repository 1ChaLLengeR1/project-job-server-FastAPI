from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.patryk.response import KeysCalculatorResponse, _to_keys_calculator_response
from database.psql.database import managed_session
from database.psql.models.patryk import KeysCalculatorPatryk


def update_calculator_keys_psql(
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
        with managed_session(db_session) as (db, _):
            row_key = db.query(KeysCalculatorPatryk).filter(KeysCalculatorPatryk.id == keys_id).first()
            if not row_key:
                return None, ApiErrorData(
                    message=f"Not found params with this id: {keys_id}",
                    type_module="update_calculator_keys_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            row_key.income_tax = float(income_tax)
            row_key.vat = float(vat)
            row_key.inpost_parcel_locker = float(inpost_parcel_locker)
            row_key.inpost_courier = float(inpost_courier)
            row_key.inpost_cash_of_delivery_courier = float(inpost_cash_of_delivery_courier)
            row_key.dpd = float(dpd)
            row_key.allegro_matt = float(allegro_matt)
            row_key.without_smart = float(without_smart)

            db.flush()
            db.refresh(row_key)
            return _to_keys_calculator_response(row_key), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="update_calculator_keys_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
