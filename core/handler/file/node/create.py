from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.node.create import create_files_node_psql
from core.repository.psql.file.node.response import FilesNodeResponse
from core.repository.psql.logs.create import create_logs_psql


def handler_create_files_node(
    user_id: str,
    name: str,
    parent_id: str | None = None,
    description: str | None = None,
    db_session: Session | None = None,
) -> tuple[FilesNodeResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = create_files_node_psql(
            name, parent_id=parent_id, description=description, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:create_node", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_create_files_node",
            type_error="exception",
            key_type_error="Exception",
        ), False
