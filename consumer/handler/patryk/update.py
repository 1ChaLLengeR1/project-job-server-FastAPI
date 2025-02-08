from consumer.data.response import ResponseData
from consumer.data.patryk.calculator.update import KeysCalculatorData
from consumer.data.user import UserData
from consumer.repository.psql.patryk.update import update_calculator_keys_psql
from consumer.helper.validators import validate_required_fields


def handler_update_calculator_keys(user_data: UserData, payload: KeysCalculatorData) -> ResponseData:
    try:

        body = ['id', 'income_tax', 'vat', 'inpost_parcel_locker', 'inpost_courier', 'inpost_cash_of_delivery_courier',
                'dpd', 'allegro_matt', 'without_smart']
        is_valid, message = validate_required_fields(payload, body)
        if not is_valid:
            return ResponseData(
                is_valid=is_valid,
                status="ERROR",
                data=message,
                status_code=400,
                additional=None,
            )

        response_update = update_calculator_keys_psql(user_data, payload)
        if not response_update['is_valid']:
            return ResponseData(
                is_valid=response_update['is_valid'],
                status=response_update['status'],
                data=response_update['data'],
                status_code=response_update['status_code'],
                additional=response_update['additional'],
            )

        return ResponseData(
            is_valid=response_update['is_valid'],
            status=response_update['status'],
            data=response_update['data'],
            status_code=response_update['status_code'],
            additional=response_update['additional'],
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=500,
            additional=None
        )
