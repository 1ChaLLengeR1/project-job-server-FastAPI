from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import FileResponse, _to_file_response
from database.psql.database import managed_session
from database.psql.models.file import File, FileStatus


def assign_file_psql(
    file_id: str,
    node_id: str,
    parent_file_id: str | None = None,
    db_session: Session | None = None,
) -> tuple[FileResponse | None, ApiErrorData | None, bool]:
    """Pierwsze przypisanie pliku do wezla - konczy upload flow (COMPLETED -> CONFIRMED).
    Wymaga statusu COMPLETED (zwraca IntegrityError/409, gdy nie jest spelniony -
    konwencja "konflikt stanu" jak w `handler_close_billing_period`). Do dalszej
    edycji juz potwierdzonego pliku (zmiana wezla, rodzica, opisu) sluzy
    `update_file_psql` - `assign_file_psql` jest tylko dla pierwszego przypisania."""
    try:
        with managed_session(db_session) as (db, _):
            file = db.query(File).filter(File.id == file_id).first()
            if not file:
                return (
                    None,
                    ApiErrorData(
                        message=f"Plik {file_id} nie istnieje.",
                        type_module="assign_file_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            if file.status != FileStatus.COMPLETED:
                return (
                    None,
                    ApiErrorData(
                        message=f"Plik {file_id} ma status {file.status.value}, wymagany completed.",
                        type_module="assign_file_psql",
                        type_error="integrity_error",
                        key_type_error="IntegrityError",
                    ),
                    False,
                )

            file.node_id = node_id
            if parent_file_id is not None:
                file.parent_file_id = parent_file_id
            file.status = FileStatus.CONFIRMED
            db.flush()
            db.refresh(file)
            return _to_file_response(file), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="assign_file_psql",
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
                type_module="assign_file_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def unassign_file_psql(
    file_id: str,
    db_session: Session | None = None,
) -> tuple[FileResponse | None, ApiErrorData | None, bool]:
    """Odwrotnosc `assign_file_psql` - odczepia plik od wezla (CONFIRMED -> COMPLETED,
    node_id -> NULL), plik wraca na liste nieprzypisanych zamiast trzeba go kasowac.
    Wymaga statusu CONFIRMED (zwraca IntegrityError/409, gdy plik nie jest przypisany -
    ta sama konwencja "konfliktu stanu" co przy `assign_file_psql`)."""
    try:
        with managed_session(db_session) as (db, _):
            file = db.query(File).filter(File.id == file_id).first()
            if not file:
                return (
                    None,
                    ApiErrorData(
                        message=f"Plik {file_id} nie istnieje.",
                        type_module="unassign_file_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            if file.status != FileStatus.CONFIRMED:
                return (
                    None,
                    ApiErrorData(
                        message=f"Plik {file_id} ma status {file.status.value}, wymagany confirmed.",
                        type_module="unassign_file_psql",
                        type_error="integrity_error",
                        key_type_error="IntegrityError",
                    ),
                    False,
                )

            file.status = FileStatus.COMPLETED
            file.node_id = None
            db.flush()
            db.refresh(file)
            return _to_file_response(file), None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="unassign_file_psql",
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
                type_module="unassign_file_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
