from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.days.response import (
    SalaryUpdateResponse,
    WorkDaysRangeUpdateResponse,
    WorkDayUpdateResponse,
)
from core.repository.psql.calendar.days.update import (
    update_day_calendary_by_id_psql,
    update_days_automatically_for_salary,
    update_days_calendary_psql,
)
from core.repository.psql.logs.create import create_logs_psql


def handler_update_day_calendary_by_id(
    user_id: str,
    day_id: str,
    norm_hours: float,
    hours_worked: float,
    hourly_rate: float,
    db_session: Session | None = None,
) -> tuple[WorkDayUpdateResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_day_calendary_by_id_psql(
            day_id, norm_hours, hours_worked, hourly_rate, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "calendar_days:update_by_id", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_update_day_calendary_by_id",
            type_error="exception",
            key_type_error="Exception",
        ), False


def handler_update_days_calendary(
    user_id: str,
    year: int,
    month: int,
    start_day: int,
    end_day: int,
    norm_hours: float,
    hours_worked: float,
    hourly_rate: float,
    db_session: Session | None = None,
) -> tuple[WorkDaysRangeUpdateResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_days_calendary_psql(
            year, month, start_day, end_day, norm_hours, hours_worked, hourly_rate, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "calendar_days:update_range", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_update_days_calendary",
            type_error="exception",
            key_type_error="Exception",
        ), False


def handler_update_days_automatically_for_salary(
    user_id: str,
    year: int,
    month: int,
    salary: float,
    db_session: Session | None = None,
) -> tuple[SalaryUpdateResponse | None, ApiErrorData | None, bool]:
    try:
        result, err, ok = update_days_automatically_for_salary(year, month, salary, db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "calendar_days:update_salary", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="handler_update_days_automatically_for_salary",
            type_error="exception",
            key_type_error="Exception",
        ), False
