from datetime import datetime

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.tasks.response import TaskStatisticsResponse
from core.repository.psql.tasks.statistics import get_task_statistics_psql


def handler_get_task_statistics_task(
    user_id: str, start_date: datetime, end_date: datetime, db_session: Session | None = None
) -> tuple[TaskStatisticsResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = get_task_statistics_psql(start_date, end_date, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "tasks:statistics", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_get_task_statistics_task",
            type_error="exception",
            key_type_error="Exception",
        ), False
