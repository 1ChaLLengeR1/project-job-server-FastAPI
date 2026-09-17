from datetime import date, timedelta

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import (
    RepositoryCollectionFilePagination,
    RepositoryCollectionFileResponse,
    _to_file_response,
)
from database.psql.database import managed_session
from database.psql.models.file import File, FilesNode, FileType


def _collect_descendant_node_ids(db: Session, node_id: str) -> list[str]:
    """BFS po drzewie wezlow (parent_id) - wezel + wszyscy potomkowie, do filtrowania
    plikow po calym poddrzewie (`recursive=True`)."""
    node_ids = [node_id]
    frontier = [node_id]
    while frontier:
        children = db.query(FilesNode.id).filter(FilesNode.parent_id.in_(frontier)).all()
        child_ids = [str(child.id) for child in children]
        if not child_ids:
            break
        node_ids.extend(child_ids)
        frontier = child_ids
    return node_ids


def collection_files_psql(
    limit: int = 32,
    offset: int = 0,
    file_type: str | None = None,
    original_name: str | None = None,
    catalog: str | None = None,
    node_id: str | None = None,
    recursive: bool = False,
    created_at_from: date | None = None,
    created_at_to: date | None = None,
    db_session: Session | None = None,
) -> tuple[RepositoryCollectionFileResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(File)

            if file_type is not None:
                query = query.filter(File.file_type == FileType(file_type))

            if original_name is not None:
                query = query.filter(File.original_name.ilike(f"%{original_name}%"))

            if catalog is not None:
                query = query.filter(File.s3_prefix == catalog)

            if node_id is not None:
                if recursive:
                    query = query.filter(File.node_id.in_(_collect_descendant_node_ids(db, node_id)))
                else:
                    query = query.filter(File.node_id == node_id)

            if created_at_from is not None:
                query = query.filter(File.created_at >= created_at_from)

            if created_at_to is not None:
                query = query.filter(File.created_at < created_at_to + timedelta(days=1))

            total = query.count()
            files = query.order_by(File.created_at.desc()).limit(limit).offset(offset).all()

            page = (offset // limit) + 1 if limit > 0 else 1

            return RepositoryCollectionFileResponse(
                data=[_to_file_response(file) for file in files],
                pagination=RepositoryCollectionFilePagination(
                    has_more=(offset + limit) < total,
                    page=page,
                    limit=limit,
                    offset=offset,
                    total=total,
                ),
            ), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="collection_files_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
