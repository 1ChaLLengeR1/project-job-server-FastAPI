from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import FileResponse, _to_file_response
from database.psql.database import managed_session
from database.psql.models.file import File, FileStatus


def confirm_file_by_id_psql(
    file_id: str, db_session: Session | None = None
) -> tuple[FileResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            file = db.query(File).filter(File.id == file_id).first()
            if not file:
                return None, ApiErrorData(
                    message=f"Plik {file_id} nie istnieje.",
                    type_module="confirm_file_by_id_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            file.status = FileStatus.COMPLETED
            db.flush()
            db.refresh(file)
            return _to_file_response(file), None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="confirm_file_by_id_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="confirm_file_by_id_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False


def update_file_psql(
    file_id: str,
    new_name: str | None = None,
    new_status: FileStatus | None = None,
    db_session: Session | None = None,
) -> tuple[FileResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            file = db.query(File).filter(File.id == file_id).first()
            if not file:
                return None, ApiErrorData(
                    message=f"Plik {file_id} nie istnieje.",
                    type_module="update_file_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            if new_name is not None:
                file.name = new_name
            if new_status is not None:
                file.status = new_status
            db.flush()
            db.refresh(file)
            return _to_file_response(file), None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="update_file_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="update_file_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
