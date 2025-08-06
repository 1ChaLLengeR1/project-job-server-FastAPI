from core.data.response import ResponseData
from database.db import get_db
from database.database_patryk.models import KeysCalculatorPatryk


def one_calculator_keys_psql() -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:
        row_key = db.query(KeysCalculatorPatryk).first()

        data = {
            "id": str(row_key.id),
            "income_tax": row_key.income_tax,
            "vat": row_key.vat,
            "inpost_parcel_locker": row_key.inpost_parcel_locker,
            "inpost_courier": row_key.inpost_courier,
            "inpost_cash_of_delivery_courier": row_key.inpost_cash_of_delivery_courier,
            "dpd": row_key.dpd,
            "allegro_matt": row_key.allegro_matt,
            "without_smart": row_key.without_smart,

        }

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=data,
            status_code=200,
            additional=None
        )
    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=417,
            additional=None
        )
    finally:
        db.close()
