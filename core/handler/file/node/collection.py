from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.node.collection import collection_files_nodes_psql
from core.repository.psql.file.node.response import FilesNodeResponse
from core.repository.psql.logs.create import create_logs_psql


def handler_collection_files_nodes(
    user_id: str, parent_id: str | None = None, all_nodes: bool = False, db_session: Session | None = None
) -> tuple[list[FilesNodeResponse] | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = collection_files_nodes_psql(parent_id=parent_id, all_nodes=all_nodes, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:collection_nodes", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_collection_files_nodes",
            type_error="exception",
            key_type_error="Exception",
        ), False
