from dataclasses import dataclass
from datetime import datetime

from database.psql.models.file import FilesNode


@dataclass
class FilesNodeResponse:
    id: str
    name: str
    parent_id: str | None
    description: str | None
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None


def _to_files_node_response(model: FilesNode) -> FilesNodeResponse:
    return FilesNodeResponse(
        id=str(model.id),
        name=model.name,
        parent_id=str(model.parent_id) if model.parent_id else None,
        description=model.description,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


@dataclass
class FilesNodeBreadcrumbItem:
    id: str
    name: str


@dataclass
class FilesNodeWithBreadcrumbResponse:
    node: FilesNodeResponse
    breadcrumb: list[FilesNodeBreadcrumbItem]
