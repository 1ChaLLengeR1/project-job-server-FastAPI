from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.node.response import (
    FilesNodeBreadcrumbItem,
    FilesNodeWithBreadcrumbResponse,
    _to_files_node_response,
)
from database.psql.database import managed_session
from database.psql.models.file import FilesNode


def _build_breadcrumb(db: Session, node: FilesNode) -> list[FilesNodeBreadcrumbItem]:
    """Sciezka od korzenia do wezla wlacznie (root -> ... -> node), krok po
    kroku w gore po `parent_id`. Prosta petla, nie BFS - to zawsze jeden
    lancuch, nie rozgalezienie (w przeciwienstwie do `_collect_descendant_node_ids`,
    ktory idzie w dol po calym poddrzewie)."""
    chain: list[FilesNodeBreadcrumbItem] = []
    current: FilesNode | None = node
    while current is not None:
        chain.append(FilesNodeBreadcrumbItem(id=str(current.id), name=current.name))
        if current.parent_id is None:
            break
        current = db.query(FilesNode).filter(FilesNode.id == current.parent_id).first()
    chain.reverse()
    return chain


def one_files_node_psql(
    node_id: str, db_session: Session | None = None
) -> tuple[FilesNodeWithBreadcrumbResponse | None, ApiErrorData | None, bool]:
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

            return FilesNodeWithBreadcrumbResponse(
                node=_to_files_node_response(node),
                breadcrumb=_build_breadcrumb(db, node),
            ), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="one_files_node_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
