from core.api.date_neger_at.get import fetch_date_nager_at_pl
from core.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import date, datetime, timedelta
from database.calendar.models import WorkDay, WorkConditionChange
from sqlalchemy.exc import IntegrityError


def statistics_calendar_psql(
        year: int
) -> ResponseData:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        row_calendary = db.query(WorkDay).filter(
            WorkDay.date >= date(year, 1, 1),
            WorkDay.date <= date(year, 12, 31)
        ).all()

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

        total_days = len(row_calendary)
        average_hours_per_working_day = total_hours_worked / working_days_count if working_days_count > 0 else 0
        average_daily_earnings = total_earnings / working_days_count if working_days_count > 0 else 0
        hours_difference = total_hours_worked - total_norm_hours
        work_efficiency = (total_hours_worked / total_norm_hours * 100) if total_norm_hours > 0 else 0

        statistics = {
            "year": year,
            "total_hours_worked": round(total_hours_worked, 2),
            "total_earnings": round(total_earnings, 2),
            "working_days_count": working_days_count,
            "total_norm_hours": round(total_norm_hours, 2),
            "hours_difference": round(hours_difference, 2),
            "total_holidays": total_holidays,
            "total_days_in_year": total_days,
            "average_hours_per_working_day": round(average_hours_per_working_day, 2),
            "average_daily_earnings": round(average_daily_earnings, 2),
            "work_efficiency_percentage": round(work_efficiency, 2)
        }

        return create_success_response(
            data=statistics,
            status_code=200
        )

    except Exception as e:
        db.rollback()
        return create_error_response(
            message=f"statistics_calendar_psql error: {e}.",
            status_code=417
        )
    finally:
        db.close()
