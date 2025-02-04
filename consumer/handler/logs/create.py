from consumer.data.response import ResponseData
from consumer.data.user import UserData
from consumer.repository.psql.logs.create import create_logs_psql


def handler_create_logs(user_data: UserData, description: str) -> ResponseData:
    try:
        response_create = create_logs_psql(user_data, description)
        if not response_create['is_valid']:
            return ResponseData(
                is_valid=response_create['is_valid'],
                status=response_create['status'],
                data=response_create['data'],
                status_code=response_create['status_code'],
                additional=response_create['additional'],
            )

        return ResponseData(
            is_valid=response_create['is_valid'],
            status=response_create['status'],
            data=response_create['data'],
            status_code=response_create['status_code'],
            additional=response_create['additional'],
        )
    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=500,
            additional=None
        )
