from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import RepositoryDeleteFileResponse, _to_delete_file_response
from database.psql.database import managed_session
from database.psql.models.file import File


def delete_file_psql(
    file_id: str, db_session: Session | None = None
) -> tuple[RepositoryDeleteFileResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            file = db.query(File).filter(File.id == file_id).first()
            if not file:
                return None, ApiErrorData(
                    message=f"Plik {file_id} nie istnieje.",
                    type_module="delete_file_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            deleted_file = _to_delete_file_response(file)
            db.delete(file)
            db.flush()
            return deleted_file, None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="delete_file_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="delete_file_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
