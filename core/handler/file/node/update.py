from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.node.response import FilesNodeResponse
from core.repository.psql.file.node.update import update_files_node_psql
from core.repository.psql.logs.create import create_logs_psql


def handler_update_files_node(
    user_id: str,
    node_id: str,
    new_name: str | None = None,
    new_description: str | None = None,
    new_parent_id: str | None = None,
    clear_parent_id: bool = False,
    new_is_active: bool | None = None,
    db_session: Session | None = None,
) -> tuple[FilesNodeResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_files_node_psql(
            node_id,
            new_name=new_name,
            new_description=new_description,
            new_parent_id=new_parent_id,
            clear_parent_id=clear_parent_id,
            new_is_active=new_is_active,
            db_session=db_session,
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:update_node", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_update_files_node",
            type_error="exception",
            key_type_error="Exception",
        ), False
