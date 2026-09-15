from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.node.response import FilesNodeResponse, _to_files_node_response
from database.psql.database import managed_session
from database.psql.models.file import FilesNode


def update_files_node_psql(
    node_id: str,
    new_name: str | None = None,
    new_description: str | None = None,
    new_parent_id: str | None = None,
    new_is_active: bool | None = None,
    db_session: Session | None = None,
) -> tuple[FilesNodeResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            node = db.query(FilesNode).filter(FilesNode.id == node_id).first()
            if not node:
                return None, ApiErrorData(
                    message=f"Węzeł {node_id} nie istnieje.",
                    type_module="update_files_node_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            if new_name is not None:
                node.name = new_name
            if new_description is not None:
                node.description = new_description
            if new_parent_id is not None:
                node.parent_id = new_parent_id
            if new_is_active is not None:
                node.is_active = new_is_active
            db.flush()
            db.refresh(node)
            return _to_files_node_response(node), None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="update_files_node_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="update_files_node_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
