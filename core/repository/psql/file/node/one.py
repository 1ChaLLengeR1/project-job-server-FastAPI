from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.node.response import FilesNodeResponse, _to_files_node_response
from database.psql.database import managed_session
from database.psql.models.file import FilesNode


def one_files_node_psql(
    node_id: str, db_session: Session | None = None
) -> tuple[FilesNodeResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            node = db.query(FilesNode).filter(FilesNode.id == node_id).first()
            if not node:
                return None, ApiErrorData(
                    message=f"Węzeł {node_id} nie istnieje.",
                    type_module="one_files_node_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            return _to_files_node_response(node), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="one_files_node_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
