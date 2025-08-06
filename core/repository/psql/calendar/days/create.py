from core.api.date_neger_at.get import fetch_date_nager_at_pl
from core.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from database.calendar.models import WorkDay
from sqlalchemy.exc import IntegrityError


def create_generator_calendar_psql(
        year: int,
        norm_hours: float,
        hourly_rate: float
) -> ResponseData:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:

        existing_count = db.query(WorkDay).filter(
            WorkDay.date >= date(year, 1, 1),
            WorkDay.date <= date(year, 12, 31)
        ).count()

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

            if current_date < today:
                hours_worked = None
            else:
                hours_worked = norm_hours

            work_day = WorkDay(
                date=current_date,
                hours_worked=hours_worked,
                is_holiday=is_holiday,
                norm_hours=norm_hours,
                hourly_rate=hourly_rate
            )
            work_day_objects.append(work_day)

            day_record = {
                "date": current_date.isoformat(),
                "hours_worked": hours_worked,
                "is_holiday": is_holiday,
                "norm_hours": norm_hours,
                "hourly_rate": hourly_rate,
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
                "year": year,
                "days_before_today": len([d for d in calendar_days if d["date"] < today.isoformat()]),
                "working_days": len([d for d in calendar_days if not d["is_holiday"]])
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
