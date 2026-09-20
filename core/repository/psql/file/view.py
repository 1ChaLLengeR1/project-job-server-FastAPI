from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import FileResponse, _to_file_response
from database.psql.database import managed_session
from database.psql.models.file import File, FileStatus


def get_viewable_file_psql(
    file_id: str, db_session: Session | None = None
) -> tuple[FileResponse | None, ApiErrorData | None, bool]:
    """Plik gotowy do podgladu/pobrania (uzywane przez preview i download -
    ten sam warunek dla obu). Wymaga statusu COMPLETED albo CONFIRMED -
    PENDING (upload w toku) i FAILED nie maja gotowego obiektu na S3."""
    try:
        with managed_session(db_session) as (db, _):
            file = db.query(File).filter(File.id == file_id).first()
            if not file:
                return None, ApiErrorData(
                    message=f"Plik {file_id} nie istnieje.",
                    type_module="get_viewable_file_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            if file.status not in (FileStatus.COMPLETED, FileStatus.CONFIRMED):
                return None, ApiErrorData(
                    message=f"Plik {file_id} ma status {file.status.value}, wymagany completed lub confirmed.",
                    type_module="get_viewable_file_psql",
                    type_error="integrity_error",
                    key_type_error="IntegrityError",
                ), False

            return _to_file_response(file), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="get_viewable_file_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
