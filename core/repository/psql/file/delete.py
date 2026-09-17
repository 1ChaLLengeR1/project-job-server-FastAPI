from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import RepositoryDeleteFileResponse, _to_delete_file_response
from database.psql.database import managed_session
from database.psql.models.file import File


def _collect_descendant_s3_keys(db: Session, file_id: str) -> list[str]:
    """BFS po plikach-dzieciach (parent_file_id). Baza usunie ich rekordy sama
    (ondelete=CASCADE), ale ich obiekty S3 trzeba posprzatac recznie - stad
    zbieranie kluczy przed usunieciem, na wszystkich poziomach zagniezdzenia."""
    s3_keys: list[str] = []
    frontier = [file_id]
    while frontier:
        children = db.query(File).filter(File.parent_file_id.in_(frontier)).all()
        if not children:
            break
        s3_keys.extend(child.s3_key for child in children)
        frontier = [str(child.id) for child in children]
    return s3_keys


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

            child_s3_keys = _collect_descendant_s3_keys(db, file_id)
            deleted_file = _to_delete_file_response(file, child_s3_keys)
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
