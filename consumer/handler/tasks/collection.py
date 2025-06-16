from consumer.repository.psql.tasks.collection import collection_tasks_psql
from consumer.data.response import ResponseData, create_error_response, create_success_response


def handler_collection_task(active: bool = True) -> ResponseData:
    try:
        response_collection = collection_tasks_psql(active)
        if not response_collection['is_valid']:
            return response_collection
        return response_collection
    except Exception as e:
        return create_error_response(message=str(e), status_code=500)
