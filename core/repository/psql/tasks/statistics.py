from datetime import datetime, timedelta
from sqlalchemy import func, cast, Date
from database.db import get_db
from database.tasks.models import Tasks
from core.data.response import ResponseData, create_success_response, create_error_response


def get_task_statistics_psql(start_date: datetime, end_date: datetime) -> ResponseData:
    db = next(get_db())
    try:
        # Wszystkie wykonane taski w podanym okresie
        tasks = db.query(Tasks).filter(
            Tasks.active == False,
            Tasks.created_at >= start_date,
            Tasks.created_at <= end_date
        ).all()

        total_tasks = len(tasks)
        total_time = sum(task.time for task in tasks)

        # Ilość tygodni w danym zakresie (uwzględniając niepełne tygodnie)
        delta_days = (end_date - start_date).days + 1
        weeks = max(delta_days / 7, 1)  # unika dzielenia przez 0

        average_per_week = total_tasks / weeks
        average_time_per_week = total_time / weeks

        # Grupowanie po dniu
        tasks_per_day_raw = (
            db.query(cast(Tasks.created_at, Date), func.count(Tasks.id))
            .filter(
                Tasks.active == False,
                Tasks.created_at >= start_date,
                Tasks.created_at <= end_date
            )
            .group_by(cast(Tasks.created_at, Date))
            .all()
        )

        # Tworzymy pusty słownik na każdy dzień
        tasks_per_day = {}
        current = start_date.date()
        while current <= end_date.date():
            tasks_per_day[str(current)] = 0
            current += timedelta(days=1)

        # Wypełniamy ilości z wyników zapytania
        for date, count in tasks_per_day_raw:
            tasks_per_day[str(date)] = count

        stats = {
            "total_tasks": total_tasks,
            "total_time": total_time,
            "average_per_week": round(average_per_week, 2),
            "average_time_per_week": round(average_time_per_week, 2),
            "tasks_per_day": tasks_per_day
        }

        return create_success_response(data=stats, status_code=200)

    except Exception as e:
        db.rollback()
        return create_error_response(message=str(e), status_code=417)
    finally:
        db.close()
