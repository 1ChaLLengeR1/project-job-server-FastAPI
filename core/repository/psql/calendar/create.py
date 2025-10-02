from core.api.date_neger_at.get import fetch_date_nager_at_pl
from core.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import date, datetime, timedelta
from database.calendar.models import WorkDay, WorkConditionChange
from sqlalchemy.exc import IntegrityError


def create_generator_calendar_psql(
        year: int
) -> ResponseData:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:

        existing_count = db.query(WorkDay).filter(
            WorkDay.date >= date(year, 1, 1),
            WorkDay.date <= date(year, 12, 31)
        ).count()

        last_work_condition = db.query(WorkConditionChange).order_by(
            desc(WorkConditionChange.created_at)
        ).first()

        if not last_work_condition:
            return create_error_response(
                message=f"Create first work condition, because database is empty.",
                status_code=400
            )

        norm_hours = float(last_work_condition.norm_hours)
        hourly_rate = float(last_work_condition.hourly_rate)

        if existing_count > 0:
            return create_error_response(
                message=f"For this year: {year} calendar existing.",
                status_code=409
            )

        raw_data, error, is_valid = fetch_date_nager_at_pl(year, "PL")
        if not is_valid:
            return create_error_response(
                message=error,
                status_code=400
            )

        holiday_days = set()
        if raw_data:
            for holiday in raw_data:
                holiday_date = datetime.strptime(holiday.date, '%Y-%m-%d').date()
                holiday_days.add(holiday_date)

        calendar_days = []
        work_day_objects = []
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        current_date = start_date
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

                if current_date < today:
                    hours_worked = norm_hours
                else:
                    hours_worked = None

            work_day = WorkDay(
                date=current_date,
                hours_worked=hours_worked,
                is_holiday=is_holiday,
                norm_hours=day_norm_hours,
                hourly_rate=day_hourly_rate
            )
            work_day_objects.append(work_day)

            day_record = {
                "date": current_date.isoformat(),
                "hours_worked": hours_worked,
                "is_holiday": is_holiday,
                "is_weekend": is_weekend,
                "norm_hours": day_norm_hours,
                "hourly_rate": day_hourly_rate,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

            calendar_days.append(day_record)
            current_date += timedelta(days=1)

        try:
            db.bulk_save_objects(work_day_objects)
            db.commit()
            inserted_count = len(work_day_objects)
        except IntegrityError as e:
            db.rollback()
            return create_error_response(
                message=f"create_generator_calendar_psql IntegrityError: {e}",
                status_code=417
            )

        response_data = {
            "calendar_days": calendar_days,
            "database_result": {
                "inserted_count": inserted_count,
            },
            "summary": {
                "total_days": len(calendar_days),
                "total_holidays": len(raw_data),
                "total_weekends": len([d for d in calendar_days if d.get("is_weekend")]),
                "year": year,
                "days_before_today": len([d for d in calendar_days if d["date"] < today.isoformat()]),
                "working_days": len([d for d in calendar_days if not d["is_holiday"] and not d.get("is_weekend")])
            }
        }

        return create_success_response(
            data=response_data,
            status_code=201
        )

    except Exception as e:
        db.rollback()
        return create_error_response(
            message=f"create_generator_calendar_psql error: {e}.",
            status_code=417
        )
    finally:
        db.close()
