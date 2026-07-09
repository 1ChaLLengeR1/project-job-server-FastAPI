from datetime import date, timedelta

from sqlalchemy import and_, desc
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.days.response import (
    AutoUpdateDaysResponse,
    AutoUpdatedDayResponse,
    ConditionUsedResponse,
    SalaryUpdatedDayResponse,
    SalaryUpdateResponse,
    WorkDaysRangeUpdateResponse,
    WorkDayUpdateResponse,
)
from database.psql.database import managed_session
from database.psql.models.calendar import WorkConditionChange, WorkDay


def update_day_calendary_by_id_psql(
    day_id: str,
    norm_hours: float,
    hours_worked: float,
    hourly_rate: float,
    db_session: Session | None = None,
) -> tuple[WorkDayUpdateResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            work_day = db.query(WorkDay).filter(WorkDay.id == day_id).first()
            if not work_day:
                return None, ApiErrorData(
                    message=f"Not found work day with this ID: {day_id}",
                    type_module="update_day_calendary_by_id_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            work_day.norm_hours = norm_hours
            work_day.hours_worked = hours_worked
            work_day.hourly_rate = hourly_rate

            db.flush()
            db.refresh(work_day)

            return WorkDayUpdateResponse(
                id=str(work_day.id),
                date=work_day.date,
                norm_hours=work_day.norm_hours,
                hours_worked=work_day.hours_worked,
                hourly_rate=work_day.hourly_rate,
                updated_at=work_day.updated_at,
            ), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="update_day_calendary_by_id_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False


def update_days_calendary_psql(
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
        with managed_session(db_session) as (db, _):
            start_date = date(year, month, start_day)
            end_date = date(year, month, end_day)

            work_days = db.query(WorkDay).filter(and_(WorkDay.date >= start_date, WorkDay.date <= end_date)).all()
            if not work_days:
                return None, ApiErrorData(
                    message=f"Not found days in this date: {start_date} - {end_date}.",
                    type_module="update_days_calendary_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            for work_day in work_days:
                work_day.norm_hours = norm_hours
                work_day.hours_worked = hours_worked
                work_day.hourly_rate = hourly_rate

            db.flush()

            return WorkDaysRangeUpdateResponse(
                updated_count=len(work_days),
                start_date=start_date,
                end_date=end_date,
                days=[day.date for day in work_days],
            ), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="update_days_calendary_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False


def update_day_automatically_psql(
    db_session: Session | None = None,
) -> tuple[AutoUpdateDaysResponse | None, ApiErrorData | None, bool]:
    """Uzupełnia zaległe dni robocze wg ostatnich warunków pracy — wołane z crona APScheduler."""
    try:
        with managed_session(db_session) as (db, _):
            today = date.today()

            latest_condition = db.query(WorkConditionChange).order_by(desc(WorkConditionChange.start_date)).first()
            if not latest_condition:
                return None, ApiErrorData(
                    message="Brak rekordów w tabeli WorkConditionChange.",
                    type_module="update_day_automatically_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            work_days = db.query(WorkDay).filter(WorkDay.date < today).all()

            updated_days: list[AutoUpdatedDayResponse] = []
            for work_day in work_days:
                if work_day.date.weekday() in [5, 6]:
                    continue

                needs_update = (
                    work_day.hours_worked is None
                    or work_day.hours_worked == 0
                    or work_day.norm_hours == 0
                    or work_day.hourly_rate == 0
                )
                if not needs_update:
                    continue

                if work_day.norm_hours == 0:
                    work_day.norm_hours = latest_condition.norm_hours
                if work_day.hourly_rate == 0:
                    work_day.hourly_rate = latest_condition.hourly_rate
                if work_day.hours_worked is None or work_day.hours_worked == 0:
                    work_day.hours_worked = latest_condition.norm_hours

                updated_days.append(
                    AutoUpdatedDayResponse(
                        id=str(work_day.id),
                        date=work_day.date,
                        norm_hours=work_day.norm_hours,
                        hours_worked=work_day.hours_worked,
                        hourly_rate=work_day.hourly_rate,
                    )
                )

            db.flush()

            return AutoUpdateDaysResponse(
                updated_count=len(updated_days),
                updated_days=updated_days,
                condition_used=ConditionUsedResponse(
                    norm_hours=latest_condition.norm_hours,
                    hourly_rate=latest_condition.hourly_rate,
                    start_date=latest_condition.start_date,
                ),
            ), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="update_day_automatically_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False


def update_days_automatically_for_salary(
    year: int, month: int, salary: float, db_session: Session | None = None
) -> tuple[SalaryUpdateResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(year, month + 1, 1) - timedelta(days=1)

            work_days = (
                db.query(WorkDay)
                .filter(
                    and_(
                        WorkDay.date >= start_date,
                        WorkDay.date <= end_date,
                        WorkDay.hours_worked > 0,
                        WorkDay.norm_hours > 0,
                    )
                )
                .all()
            )
            if not work_days:
                return None, ApiErrorData(
                    message=f"Brak dni roboczych z godzinami w {year}-{month:02d}",
                    type_module="update_days_automatically_for_salary",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            total_hours_worked = sum(day.hours_worked for day in work_days)
            if total_hours_worked == 0:
                return None, ApiErrorData(
                    message=f"Suma godzin przepracowanych wynosi 0 w {year}-{month:02d}",
                    type_module="update_days_automatically_for_salary",
                    type_error="validation_error",
                    key_type_error="Exception",
                ), False

            calculated_hourly_rate = salary / total_hours_worked

            updated_days: list[SalaryUpdatedDayResponse] = []
            for work_day in work_days:
                work_day.hourly_rate = calculated_hourly_rate
                updated_days.append(
                    SalaryUpdatedDayResponse(
                        id=str(work_day.id),
                        date=work_day.date,
                        hours_worked=work_day.hours_worked,
                        hourly_rate=work_day.hourly_rate,
                        daily_salary=round(work_day.hours_worked * work_day.hourly_rate, 2),
                    )
                )

            db.flush()

            # Weryfikacja sumy po przeliczeniu stawki
            total_salary = sum(day.hours_worked * day.hourly_rate for day in work_days)

            return SalaryUpdateResponse(
                updated_count=len(updated_days),
                total_hours_worked=total_hours_worked,
                calculated_hourly_rate=round(calculated_hourly_rate, 2),
                expected_salary=salary,
                actual_total_salary=round(total_salary, 2),
                updated_days=updated_days,
            ), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="update_days_automatically_for_salary",
            type_error="exception",
            key_type_error="Exception",
        ), False
