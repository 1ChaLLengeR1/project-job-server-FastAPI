from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import FileWithChildrenResponse, _to_file_response
from database.psql.database import managed_session
from database.psql.models.file import File


def one_file_psql(
    file_id: str, db_session: Session | None = None
) -> tuple[FileWithChildrenResponse | None, ApiErrorData | None, bool]:
    """Szczegoly pliku + lista plikow-dzieci (`parent_file_id`). Bez breadcrumb
    wezla na razie - ta sama, wczesniej ustalona decyzja co przy `GET
    /files/nodes/one/{node_id}`."""
    try:
        with managed_session(db_session) as (db, _):
            file = db.query(File).filter(File.id == file_id).first()
            if not file:
                return None, ApiErrorData(
                    message=f"Plik {file_id} nie istnieje.",
                    type_module="one_file_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            children = db.query(File).filter(File.parent_file_id == file_id).order_by(File.created_at).all()

            return FileWithChildrenResponse(
                file=_to_file_response(file),
                children=[_to_file_response(child) for child in children],
            ), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="one_file_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
