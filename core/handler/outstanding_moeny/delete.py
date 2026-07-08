from core.data.response import ResponseData
from core.data.user import UserData
from core.repository.psql.outstanding_moeny.delete import delete_item_psql, delete_list_psql


def handler_delete_list(user_data: UserData, id: str) -> ResponseData:
    try:
        response_delete = delete_list_psql(user_data, id)
        if not response_delete["is_valid"]:
            return ResponseData(
                is_valid=response_delete["is_valid"],
                status=response_delete["status"],
                data=response_delete["data"],
                status_code=response_delete["status_code"],
                additional=response_delete["additional"],
            )

        return ResponseData(
            is_valid=response_delete["is_valid"],
            status=response_delete["status"],
            data=response_delete["data"],
            status_code=response_delete["status_code"],
            additional=response_delete["additional"],
        )
    except Exception as e:
        return ResponseData(is_valid=False, status="ERROR", data=str(e), status_code=500, additional=None)


def handler_delete_item(user_data: UserData, id: str) -> ResponseData:
    try:
        response_delete = delete_item_psql(user_data, id)
        if not response_delete["is_valid"]:
            return ResponseData(
                is_valid=response_delete["is_valid"],
                status=response_delete["status"],
                data=response_delete["data"],
                status_code=response_delete["status_code"],
                additional=response_delete["additional"],
            )

        return ResponseData(
            is_valid=response_delete["is_valid"],
            status=response_delete["status"],
            data=response_delete["data"],
            status_code=response_delete["status_code"],
            additional=response_delete["additional"],
        )
    except Exception as e:
        return ResponseData(is_valid=False, status="ERROR", data=str(e), status_code=500, additional=None)
