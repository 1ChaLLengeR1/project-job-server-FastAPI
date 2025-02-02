from consumer.data.response import ResponseData
from consumer.repository.psql.outstanding_moeny.create import create_list_psql, add_item_psql
from consumer.data.outstanding_moeny.create import CreateListParams, AddItemParams
from consumer.data.user import UserData


def handler_create_list(user_data: UserData, payload: CreateListParams) -> ResponseData:
    try:
        response_create = create_list_psql(user_data, payload)
        if not response_create['is_valid']:
            return ResponseData(
                is_valid=response_create['is_valid'],
                status=response_create['status'],
                data=response_create['data'],
                status_code=response_create['status_code'],
                additional=response_create['additional']
            )

        return ResponseData(
            is_valid=response_create['is_valid'],
            status=response_create['status'],
            data=response_create['data'],
            status_code=response_create['status_code'],
            additional=response_create['additional']
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=500,
            additional=None
        )


def handler_add_item(user_data: UserData, payload: AddItemParams) -> ResponseData:
    try:
        response_create = add_item_psql(user_data, payload)
        if not response_create['is_valid']:
            return ResponseData(
                is_valid=response_create['is_valid'],
                status=response_create['status'],
                data=response_create['data'],
                status_code=response_create['status_code'],
                additional=response_create['additional']
            )

        return ResponseData(
            is_valid=response_create['is_valid'],
            status=response_create['status'],
            data=response_create['data'],
            status_code=response_create['status_code'],
            additional=response_create['additional']
        )
    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=500,
            additional=None
        )
