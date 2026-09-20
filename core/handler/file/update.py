from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import FileResponse
from core.repository.psql.file.update import confirm_file_by_id_psql, update_file_psql
from core.repository.psql.logs.create import create_logs_psql
from database.psql.models.file import FileStatus


def handler_update_file(
    user_id: str,
    file_id: str,
    status: FileStatus | None = None,
    name: str | None = None,
    db_session: Session | None = None,
) -> tuple[FileResponse | None, ApiErrorData | None, bool]:
    try:
        # "confirmed" to sygnal od frontendu "upload zakonczony" - realnie ustawia COMPLETED
        # (zob. status pliku w docs/PLAN_MAGAZYN_PLIKOW.md); kazdy inny status/nazwa idzie
        # przez ogolny update.
        if status == FileStatus.CONFIRMED:
            result, err, ok = confirm_file_by_id_psql(file_id, db_session=db_session)
        else:
            result, err, ok = update_file_psql(file_id, new_name=name, new_status=status, db_session=db_session)

        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:update", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_update_file",
            type_error="exception",
            key_type_error="Exception",
        ), False
