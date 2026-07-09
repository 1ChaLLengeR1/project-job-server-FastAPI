from datetime import datetime, timedelta

from sqlalchemy import Date, cast, func
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.tasks.response import TaskStatisticsResponse
from database.psql.database import managed_session
from database.psql.models.tasks import Tasks


def get_task_statistics_psql(
    start_date: datetime, end_date: datetime, db_session: Session | None = None
) -> tuple[TaskStatisticsResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            # Wszystkie wykonane taski w podanym okresie
            tasks = (
                db.query(Tasks)
                .filter(Tasks.active.is_(False), Tasks.created_at >= start_date, Tasks.created_at <= end_date)
                .all()
            )

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
                .filter(Tasks.active.is_(False), Tasks.created_at >= start_date, Tasks.created_at <= end_date)
                .group_by(cast(Tasks.created_at, Date))
                .all()
            )

            # Pusty słownik na każdy dzień zakresu, potem ilości z zapytania
            tasks_per_day = {}
            current = start_date.date()
            while current <= end_date.date():
                tasks_per_day[str(current)] = 0
                current += timedelta(days=1)

            for date, count in tasks_per_day_raw:
                tasks_per_day[str(date)] = count

            return TaskStatisticsResponse(
                total_tasks=total_tasks,
                total_time=total_time,
                average_per_week=round(average_per_week, 2),
                average_time_per_week=round(average_time_per_week, 2),
                tasks_per_day=tasks_per_day,
            ), None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="get_task_statistics_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
