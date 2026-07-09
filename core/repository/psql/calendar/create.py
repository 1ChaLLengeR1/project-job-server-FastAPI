from datetime import date, timedelta

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.response import (
    GeneratedCalendarResponse,
    GeneratedCalendarSummaryResponse,
    GeneratedDayResponse,
)
from database.psql.database import managed_session
from database.psql.models.calendar import WorkConditionChange, WorkDay


def create_generator_calendar_psql(
    year: int, holiday_days: set[date], db_session: Session | None = None
) -> tuple[GeneratedCalendarResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            existing_count = (
                db.query(WorkDay).filter(WorkDay.date >= date(year, 1, 1), WorkDay.date <= date(year, 12, 31)).count()
            )
            if existing_count > 0:
                return None, ApiErrorData(
                    message=f"For this year: {year} calendar existing.",
                    type_module="create_generator_calendar_psql",
                    type_error="integrity_error",
                    key_type_error="IntegrityError",
                ), False

            last_work_condition = db.query(WorkConditionChange).order_by(desc(WorkConditionChange.created_at)).first()
            if not last_work_condition:
                return None, ApiErrorData(
                    message="Create first work condition, because database is empty.",
                    type_module="create_generator_calendar_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            norm_hours = float(last_work_condition.norm_hours)
            hourly_rate = float(last_work_condition.hourly_rate)

            calendar_days: list[GeneratedDayResponse] = []
            work_day_objects = []
            end_date = date(year, 12, 31)
            current_date = date(year, 1, 1)
            today = date.today()

            while current_date <= end_date:
                is_holiday = current_date in holiday_days
                is_weekend = current_date.weekday() in [5, 6]

                if is_weekend:
                    day_norm_hours = 0
                    day_hourly_rate = 0
                    hours_worked = 0
                else:
                    day_norm_hours = norm_hours
                    day_hourly_rate = hourly_rate
                    hours_worked = norm_hours if current_date < today else None

                work_day_objects.append(
                    WorkDay(
                        date=current_date,
                        hours_worked=hours_worked,
                        is_holiday=is_holiday,
                        norm_hours=day_norm_hours,
                        hourly_rate=day_hourly_rate,
                    )
                )
                calendar_days.append(
                    GeneratedDayResponse(
                        date=current_date,
                        hours_worked=hours_worked,
                        is_holiday=is_holiday,
                        is_weekend=is_weekend,
                        norm_hours=day_norm_hours,
                        hourly_rate=day_hourly_rate,
                    )
                )
                current_date += timedelta(days=1)

            db.bulk_save_objects(work_day_objects)
            db.flush()

            summary = GeneratedCalendarSummaryResponse(
                total_days=len(calendar_days),
                total_holidays=len(holiday_days),
                total_weekends=len([d for d in calendar_days if d.is_weekend]),
                year=year,
                days_before_today=len([d for d in calendar_days if d.date < today]),
                working_days=len([d for d in calendar_days if not d.is_holiday and not d.is_weekend]),
            )

            return GeneratedCalendarResponse(
                calendar_days=calendar_days,
                inserted_count=len(work_day_objects),
                summary=summary,
            ), None, True

    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="create_generator_calendar_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="create_generator_calendar_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
