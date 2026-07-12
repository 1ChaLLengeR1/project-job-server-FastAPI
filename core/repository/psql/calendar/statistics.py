from datetime import date

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.response import CalendarStatisticsResponse
from database.psql.database import managed_session
from database.psql.models.calendar import WorkDay


def statistics_calendar_psql(
    year: int, db_session: Session | None = None
) -> tuple[CalendarStatisticsResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            row_calendary = (
                db.query(WorkDay).filter(WorkDay.date >= date(year, 1, 1), WorkDay.date <= date(year, 12, 31)).all()
            )

            total_hours_worked = 0.0
            total_earnings = 0.0
            working_days_count = 0
            total_norm_hours = 0.0
            total_holidays = 0

            for day in row_calendary:
                if day.hours_worked and day.hours_worked > 0:
                    total_hours_worked += day.hours_worked
                    total_earnings += day.hours_worked * day.hourly_rate
                    working_days_count += 1

                total_norm_hours += day.norm_hours

                if day.is_holiday:
                    total_holidays += 1

            average_hours_per_working_day = total_hours_worked / working_days_count if working_days_count > 0 else 0
            average_daily_earnings = total_earnings / working_days_count if working_days_count > 0 else 0
            work_efficiency = (total_hours_worked / total_norm_hours * 100) if total_norm_hours > 0 else 0

            return CalendarStatisticsResponse(
                year=year,
                total_hours_worked=round(total_hours_worked, 2),
                total_earnings=round(total_earnings, 2),
                working_days_count=working_days_count,
                total_norm_hours=round(total_norm_hours, 2),
                hours_difference=round(total_hours_worked - total_norm_hours, 2),
                total_holidays=total_holidays,
                total_days_in_year=len(row_calendary),
                average_hours_per_working_day=round(average_hours_per_working_day, 2),
                average_daily_earnings=round(average_daily_earnings, 2),
                work_efficiency_percentage=round(work_efficiency, 2),
            ), None, True

    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="statistics_calendar_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
