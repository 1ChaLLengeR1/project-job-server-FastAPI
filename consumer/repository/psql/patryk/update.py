from consumer.data.response import ResponseData
from database.db import get_db
from database.database_patryk.models import KeysCalculatorPatryk
from consumer.data.patryk.calculator.update import KeysCalculatorData
from consumer.data.user import UserData
from consumer.repository.psql.user.check import check_user_role_psql


def update_calculator_keys_psql(user_data: UserData, payload: KeysCalculatorData) -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:
        check_role = check_user_role_psql(user_data, 'admin')
        if not check_role['is_valid']:
            return ResponseData(
                is_valid=check_role['is_valid'],
                status=check_role['status'],
                data=check_role['data'],
                status_code=check_role['status_code'],
                additional=check_role['additional']
            )

        row_key = db.query(KeysCalculatorPatryk).filter(KeysCalculatorPatryk.id == payload['id']).first()
        if not row_key:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=str(f"Not found params with this id: {payload['id']}"),
                status_code=400,
                additional=None
            )

        row_key.income_tax = float(payload['income_tax'])
        row_key.vat = float(payload['vat'])
        row_key.inpost_parcel_locker = float(payload['inpost_parcel_locker'])
        row_key.inpost_courier = float(payload['inpost_courier'])
        row_key.inpost_cash_of_delivery_courier = float(payload['inpost_cash_of_delivery_courier'])
        row_key.dpd = float(payload['dpd'])
        row_key.allegro_matt = float(payload['allegro_matt'])
        row_key.without_smart = float(payload['without_smart'])

        db.commit()

        updated_data = {
            "id": row_key.id,
            "income_tax": row_key.income_tax,
            "vat": row_key.vat,
            "inpost_parcel_locker": row_key.inpost_parcel_locker,
            "inpost_courier": row_key.inpost_courier,
            "inpost_cash_of_delivery_courier": row_key.inpost_cash_of_delivery_courier,
            "dpd": row_key.dpd,
            "allegro_matt": row_key.allegro_matt,
            "without_smart": row_key.without_smart
        }

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=updated_data,
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
