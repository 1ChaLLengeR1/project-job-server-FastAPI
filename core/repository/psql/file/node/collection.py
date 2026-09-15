from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.node.response import FilesNodeResponse, _to_files_node_response
from database.psql.database import managed_session
from database.psql.models.file import FilesNode


def collection_files_nodes_psql(
    parent_id: str | None = None, db_session: Session | None = None
) -> tuple[list[FilesNodeResponse] | None, ApiErrorData | None, bool]:
    """Zwraca dzieci danego wezla; `parent_id=None` = wezly najwyzszego poziomu.

    Na razie jeden poziom na zapytanie (bez rekursji po poddrzewie) - podstawowa
    wersja pod dalsza rozbudowe (zob. PLAN_MAGAZYN_PLIKOW.md, etap 3/6).
    """
    try:
        with managed_session(db_session) as (db, _):
            nodes = (
                db.query(FilesNode)
                .filter(FilesNode.parent_id == parent_id)
                .order_by(FilesNode.name)
                .all()
            )
            return [_to_files_node_response(node) for node in nodes], None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="collection_files_nodes_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
