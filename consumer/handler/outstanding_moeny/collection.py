from consumer.data.response import ResponseData
from consumer.repository.psql.outstanding_moeny.collection import collection_list_psql


def handler_collection_list() -> ResponseData:
    try:
        response_collection = collection_list_psql()
        if not response_collection['is_valid']:
            return ResponseData(
                is_valid=response_collection['is_valid'],
                status=response_collection['status'],
                data=response_collection['data'],
                status_code=response_collection['status_code'],
                additional=response_collection['additional']
            )

        return ResponseData(
            is_valid=response_collection['is_valid'],
            status=response_collection['status'],
            data=response_collection['data'],
            status_code=response_collection['status_code'],
            additional=response_collection['additional']
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=500,
            additional=None
        )
