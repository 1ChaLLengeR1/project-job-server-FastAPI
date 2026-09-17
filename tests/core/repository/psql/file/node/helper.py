from uuid import uuid4

from sqlalchemy.orm import Session

from database.psql.models.file import FilesNode


def make_files_node(
    db: Session,
    *,
    name: str | None = None,
    parent_id: str | None = None,
    description: str | None = None,
    is_active: bool = True,
) -> FilesNode:
    node = FilesNode(
        name=name or f"węzeł_{uuid4().hex[:8]}",
        parent_id=parent_id,
        description=description,
        is_active=is_active,
    )
    db.add(node)
    db.flush()
    return node
