from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.node.response import FilesNodeResponse, _to_files_node_response
from database.psql.database import managed_session
from database.psql.models.file import FilesNode


def create_files_node_psql(
    name: str,
    parent_id: str | None = None,
    description: str | None = None,
    db_session: Session | None = None,
) -> tuple[FilesNodeResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_node = FilesNode(name=name, parent_id=parent_id, description=description)
            db.add(new_node)
            db.flush()
            db.refresh(new_node)
            return _to_files_node_response(new_node), None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="create_files_node_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="create_files_node_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
