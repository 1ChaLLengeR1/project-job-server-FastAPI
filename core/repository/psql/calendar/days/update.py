from core.api.date_neger_at.get import fetch_date_nager_at_pl
from core.data.response import ResponseData, create_success_response, create_error_response
from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import date, datetime, timedelta
from database.calendar.models import WorkDay, WorkConditionChange
from sqlalchemy.exc import IntegrityError


def update_day_calendary_by_id_psql(
        day_id: str,
        norm_hours: float,
        hours_worked: float,
        hourly_rate: float,
) -> ResponseData:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        work_day = db.query(WorkDay).filter(WorkDay.id == day_id).first()
        if not work_day:
            return create_error_response(
                message=f"Not found work day with this ID: {day_id}",
                status_code=400
            )

        work_day.norm_hours = norm_hours
        work_day.hours_worked = hours_worked
        work_day.hourly_rate = hourly_rate
        work_day.updated_at = datetime.now()

        db.commit()
        db.refresh(work_day)

        return create_success_response(
            data={
                "id": str(work_day.id),
                "date": work_day.date.isoformat(),
                "norm_hours": work_day.norm_hours,
                "hours_worked": work_day.hours_worked,
                "hourly_rate": work_day.hourly_rate,
                "updated_at": work_day.updated_at.isoformat()
            }
        )

    except Exception as e:
        return create_error_response(
            message=f"update_day_calendary_by_id_psql Exception: {str(e)}",
            status_code=417
        )
    finally:
        db.close()


def update_days_calendary_psql(
        year: int,
        month: int,
        start_day: int,
        end_day: int,
        norm_hours: float,
        hours_worked: float,
        hourly_rate: float,
) -> ResponseData:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        start_date = date(year, month, start_day)
        end_date = date(year, month, end_day)

        work_days = db.query(WorkDay).filter(
            and_(
                WorkDay.date >= start_date,
                WorkDay.date <= end_date
            )
        ).all()

        if not work_days:
            return create_error_response(
                message=f"Not found days in this date: {start_date} - {end_date}.",
                status_code=400
            )

        updated_count = 0
        for work_day in work_days:
            work_day.norm_hours = norm_hours
            work_day.hours_worked = hours_worked
            work_day.hourly_rate = hourly_rate
            work_day.updated_at = datetime.now()
            updated_count += 1

        db.commit()
        return create_success_response(
            data={
                "updated_count": updated_count,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": [day.date.isoformat() for day in work_days]
            }
        )

    except Exception as e:
        return create_error_response(
            message=f"update_days_calendary_psql Exception: {str(e)}",
            status_code=417
        )
    finally:
        db.close()


def update_day_automatically_psql() -> ResponseData:
    db_generator = get_db()
    db: Session = next(db_generator)
    try:
        today = date.today()

        latest_condition = db.query(WorkConditionChange).order_by(
            desc(WorkConditionChange.start_date)
        ).first()

        if not latest_condition:
            return create_error_response(
                message="Brak rekordów w tabeli WorkConditionChange.",
                status_code=404
            )

        work_days = db.query(WorkDay).filter(
            WorkDay.date < today
        ).all()

        updated_count = 0
        updated_days = []

        for work_day in work_days:
            if work_day.date.weekday() in [5, 6]:
                continue

            needs_update = (
                    work_day.hours_worked is None or
                    work_day.hours_worked == 0 or
                    work_day.norm_hours == 0 or
                    work_day.hourly_rate == 0
            )

            if needs_update:
                if work_day.norm_hours == 0:
                    work_day.norm_hours = latest_condition.norm_hours

                if work_day.hourly_rate == 0:
                    work_day.hourly_rate = latest_condition.hourly_rate

                if work_day.hours_worked is None or work_day.hours_worked == 0:
                    work_day.hours_worked = latest_condition.norm_hours

                work_day.updated_at = datetime.now()
                updated_count += 1
                updated_days.append({
                    "id": str(work_day.id),
                    "date": work_day.date.isoformat(),
                    "norm_hours": work_day.norm_hours,
                    "hours_worked": work_day.hours_worked,
                    "hourly_rate": work_day.hourly_rate
                })

        db.commit()

        return create_success_response(
            data={
                "updated_count": updated_count,
                "updated_days": updated_days,
                "condition_used": {
                    "norm_hours": latest_condition.norm_hours,
                    "hourly_rate": latest_condition.hourly_rate,
                    "start_date": latest_condition.start_date.isoformat()
                }
            },
            status_code=200
        )

    except Exception as e:
        db.rollback()
        return create_error_response(
            message=f"update_day_automatically_psql Exception: {str(e)}",
            status_code=417
        )
    finally:
        db.close()
