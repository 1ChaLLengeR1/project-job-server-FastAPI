from core.data.response import ResponseData
from core.repository.psql.outstanding_moeny.update import edit_name_list_psql, edit_item_psql
from core.data.outstanding_moeny.update import EditListParams, EditItem
from core.data.user import UserData


def handler_edit_name_list(user_data: UserData, payload: EditListParams) -> ResponseData:
    try:
        response = edit_name_list_psql(user_data, payload)
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


def handler_edit_item(user_data: UserData, payload: EditItem) -> ResponseData:
    try:
        response = edit_item_psql(user_data, payload)
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
