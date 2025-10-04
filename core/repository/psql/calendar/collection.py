from core.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc, extract
from datetime import date, datetime, timedelta
from database.calendar.models import WorkDay
from sqlalchemy.exc import IntegrityError
from collections import defaultdict


def collection_calendar_psql(
        year: int,
        month: int
) -> ResponseData:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        row_collection = db.query(WorkDay).filter(
            extract('year', WorkDay.date) == year,
            extract('month', WorkDay.date) == month
        ).order_by(WorkDay.date.asc()).all()

        if not row_collection:
            return create_error_response(
                message=f"For this year: {year} and month: {month} is not available.",
                status_code=400
            )

        days_data = []
        weeks_data = defaultdict(list)

        day_names = {
            0: 'poniedziałek',
            1: 'wtorek',
            2: 'środa',
            3: 'czwartek',
            4: 'piątek',
            5: 'sobota',
            6: 'niedziela'
        }

        for work_day in row_collection:
            day_info = {
                'id': str(work_day.id),
                'date': work_day.date.isoformat(),
                'day_number': work_day.date.day,
                'day_name': day_names[work_day.date.weekday()],
                'hours_worked': work_day.hours_worked or 0,
                'is_holiday': work_day.is_holiday,
                'norm_hours': work_day.norm_hours,
                'hourly_rate': work_day.hourly_rate,
                'daily_salary': (work_day.hours_worked or 0) * work_day.hourly_rate
            }
            days_data.append(day_info)

            week_number = work_day.date.isocalendar()[1]
            weeks_data[week_number].append(day_info)

        weeks_statistics = []
        total_hours_month = 0
        total_norm_hours_month = 0
        total_salary_month = 0

        for week_num in sorted(weeks_data.keys()):
            week_days = weeks_data[week_num]
            week_hours = sum(day['hours_worked'] for day in week_days)
            week_norm_hours = sum(day['norm_hours'] for day in week_days)

            hourly_rate = week_days[0]['hourly_rate'] if week_days else 0
            week_salary = week_hours * hourly_rate

            total_hours_month += week_hours
            total_norm_hours_month += week_norm_hours
            total_salary_month += week_salary

            weeks_statistics.append({
                'week_number': week_num,
                'total_hours': week_hours,
                'total_norm_hours': week_norm_hours,
                'hourly_rate': hourly_rate,
                'salary': week_salary
            })

        month_names = {
            1: 'Styczeń', 2: 'Luty', 3: 'Marzec', 4: 'Kwiecień',
            5: 'Maj', 6: 'Czerwiec', 7: 'Lipiec', 8: 'Sierpień',
            9: 'Wrzesień', 10: 'Październik', 11: 'Listopad', 12: 'Grudzień'
        }

        return create_success_response(
            data={
                'year': year,
                'month': month,
                'month_name': month_names.get(month, ''),
                'days': days_data,
                'statistics': {
                    'total_hours_worked': total_hours_month,
                    'total_norm_hours': total_norm_hours_month,
                    'total_salary': total_salary_month,
                    'weeks': weeks_statistics
                }
            }
        )

    except Exception as e:
        db.rollback()
        return create_error_response(
            message=f"collection_calendar_psql error: {e}.",
            status_code=417
        )
    finally:
        db.close()
