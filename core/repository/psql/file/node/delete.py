from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.node.response import FilesNodeResponse, _to_files_node_response
from database.psql.database import managed_session
from database.psql.models.file import FilesNode


def delete_files_node_psql(
    node_id: str, db_session: Session | None = None
) -> tuple[FilesNodeResponse | None, ApiErrorData | None, bool]:
    """Usuwa wezel. RESTRICT z bazy (FK) blokuje usuniecie, gdy wezel ma dzieci-wezly
    lub przypisane pliki (files.node_id) - taki przypadek wraca jako IntegrityError/409."""
    try:
        with managed_session(db_session) as (db, _):
            node = db.query(FilesNode).filter(FilesNode.id == node_id).first()
            if not node:
                return None, ApiErrorData(
                    message=f"Węzeł {node_id} nie istnieje.",
                    type_module="delete_files_node_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            deleted_node = _to_files_node_response(node)
            db.delete(node)
            db.flush()
            return deleted_node, None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="delete_files_node_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="delete_files_node_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
