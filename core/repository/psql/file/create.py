from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import FileResponse, _to_file_response
from database.psql.database import managed_session
from database.psql.models.file import File, FileType


def create_file_psql(
    user_id: str,
    name: str,
    original_name: str,
    size: int,
    file_type: FileType,
    mime_type: str,
    s3_key: str,
    s3_prefix: str,
    url: str,
    db_session: Session | None = None,
) -> tuple[FileResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            new_file = File(
                user_id=user_id,
                name=name,
                original_name=original_name,
                size=size,
                file_type=file_type,
                mime_type=mime_type,
                s3_key=s3_key,
                s3_prefix=s3_prefix,
                url=url,
            )
            db.add(new_file)
            db.flush()
            db.refresh(new_file)
            return _to_file_response(new_file), None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="create_file_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="create_file_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
