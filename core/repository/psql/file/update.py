from datetime import date

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
                return (
                    None,
                    ApiErrorData(
                        message=f"Plik {file_id} nie istnieje.",
                        type_module="confirm_file_by_id_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            file.status = FileStatus.COMPLETED
            db.flush()
            db.refresh(file)
            return _to_file_response(file), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="confirm_file_by_id_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="confirm_file_by_id_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def update_file_psql(
    file_id: str,
    new_name: str | None = None,
    new_status: FileStatus | None = None,
    new_original_name: str | None = None,
    new_node_id: str | None = None,
    new_parent_file_id: str | None = None,
    clear_parent_file_id: bool = False,
    new_description: str | None = None,
    clear_description: bool = False,
    new_guarantee_start_date: date | None = None,
    clear_guarantee_start_date: bool = False,
    new_guarantee_end_date: date | None = None,
    clear_guarantee_end_date: bool = False,
    db_session: Session | None = None,
) -> tuple[FileResponse | None, ApiErrorData | None, bool]:
    """Ogolny partial update ("metadane" pliku juz po uploadzie): `None` = nie
    dotykaj pola. Pola nullable (`parent_file_id`, `description`, daty gwarancji)
    maja dedykowane `clear_*` flagi, bo `None` jest juz zajete pod "nie zmieniaj"
    (ten sam trick co przy `update_files_node_psql`). `node_id` celowo NIE ma
    odpowiednika `clear_node_id` - tej funkcji nie da sie uzyc do odczepienia
    potwierdzonego pliku od wezla; pierwsze przypisanie robi `assign_file_psql`,
    a baza i tak pilnuje niezmiennika CHECK-iem `ck_files_confirmed_requires_node`.
    """
    try:
        with managed_session(db_session) as (db, _):
            file = db.query(File).filter(File.id == file_id).first()
            if not file:
                return (
                    None,
                    ApiErrorData(
                        message=f"Plik {file_id} nie istnieje.",
                        type_module="update_file_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            if new_name is not None:
                file.name = new_name
            if new_status is not None:
                file.status = new_status
            if new_original_name is not None:
                file.original_name = new_original_name
            if new_node_id is not None:
                file.node_id = new_node_id
            if clear_parent_file_id:
                file.parent_file_id = None
            elif new_parent_file_id is not None:
                file.parent_file_id = new_parent_file_id
            if clear_description:
                file.description = None
            elif new_description is not None:
                file.description = new_description
            if clear_guarantee_start_date:
                file.guarantee_start_date = None
            elif new_guarantee_start_date is not None:
                file.guarantee_start_date = new_guarantee_start_date
            if clear_guarantee_end_date:
                file.guarantee_end_date = None
            elif new_guarantee_end_date is not None:
                file.guarantee_end_date = new_guarantee_end_date
            db.flush()
            db.refresh(file)
            return _to_file_response(file), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="update_file_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="update_file_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
