from datetime import date

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.file.response import FileResponse
from core.repository.psql.file.update import update_file_psql
from core.repository.psql.logs.create import create_logs_psql


def handler_update_file_metadata(
    user_id: str,
    file_id: str,
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
    try:
        result, err, ok = update_file_psql(
            file_id,
            new_original_name=new_original_name,
            new_node_id=new_node_id,
            new_parent_file_id=new_parent_file_id,
            clear_parent_file_id=clear_parent_file_id,
            new_description=new_description,
            clear_description=clear_description,
            new_guarantee_start_date=new_guarantee_start_date,
            clear_guarantee_start_date=clear_guarantee_start_date,
            new_guarantee_end_date=new_guarantee_end_date,
            clear_guarantee_end_date=clear_guarantee_end_date,
            db_session=db_session,
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "files:update_metadata", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_update_file_metadata",
            type_error="exception",
            key_type_error="Exception",
        ), False
