from consumer.data.response import ResponseData
from consumer.data.user import UserData
from consumer.repository.psql.logs.collection import collection_logs_psql


def handler_collection_logs(number: int) -> ResponseData:
    try:
        response = collection_logs_psql(number)
        if not response['is_valid']:
            return ResponseData(
                is_valid=response['is_valid'],
                status=response['status'],
                data=response['data'],
                status_code=response['status_code'],
                additional=response['additional'],
            )

        return ResponseData(
            is_valid=response['is_valid'],
            status=response['status'],
            data=response['data'],
            status_code=response['status_code'],
            additional=response['additional'],
        )
    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=500,
            additional=None
        )
