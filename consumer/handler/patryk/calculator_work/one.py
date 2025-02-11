from consumer.data.response import ResponseData
from consumer.repository.psql.patryk.one import one_calculator_keys_psql


def handler_one_calculator_keys() -> ResponseData:
    try:
        response = one_calculator_keys_psql()
        if not response['is_valid']:
            return ResponseData(
                is_valid=response['is_valid'],
                status=response['status'],
                data=response['data'],
                status_code=response['status_code'],
                additional=response['additional']
            )

        return ResponseData(
            is_valid=response['is_valid'],
            status=response['status'],
            data=response['data'],
            status_code=response['status_code'],
            additional=response['additional']
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=500,
            additional=None
        )
