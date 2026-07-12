from datetime import date

from sqlalchemy.orm import Session

from database.psql.models.calendar import WorkConditionChange, WorkDay


def make_condition(
    db: Session,
    *,
    norm_hours: float = 8.0,
    hourly_rate: float = 30.0,
    start_date: date | None = None,
) -> WorkConditionChange:
    condition = WorkConditionChange(
        start_date=start_date or date.today(), norm_hours=norm_hours, hourly_rate=hourly_rate
    )
    db.add(condition)
    db.flush()
    return condition


def make_work_day(
    db: Session,
    *,
    day: date,
    hours_worked: float | None = 8.0,
    norm_hours: float = 8.0,
    hourly_rate: float = 30.0,
    is_holiday: bool = False,
) -> WorkDay:
    work_day = WorkDay(
        date=day,
        hours_worked=hours_worked,
        norm_hours=norm_hours,
        hourly_rate=hourly_rate,
        is_holiday=is_holiday,
    )
    db.add(work_day)
    db.flush()
    return work_day
