from collections import defaultdict

from sqlalchemy import extract
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.calendar.response import (
    CalendarCollectionResponse,
    CalendarDayResponse,
    MonthStatisticsResponse,
    WeekStatisticsResponse,
)
from database.psql.database import managed_session
from database.psql.models.calendar import WorkDay

_DAY_NAMES = {
    0: "poniedziałek",
    1: "wtorek",
    2: "środa",
    3: "czwartek",
    4: "piątek",
    5: "sobota",
    6: "niedziela",
}

_MONTH_NAMES = {
    1: "Styczeń",
    2: "Luty",
    3: "Marzec",
    4: "Kwiecień",
    5: "Maj",
    6: "Czerwiec",
    7: "Lipiec",
    8: "Sierpień",
    9: "Wrzesień",
    10: "Październik",
    11: "Listopad",
    12: "Grudzień",
}


def collection_calendar_psql(
    year: int, month: int, db_session: Session | None = None
) -> tuple[CalendarCollectionResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            row_collection = (
                db.query(WorkDay)
                .filter(extract("year", WorkDay.date) == year, extract("month", WorkDay.date) == month)
                .order_by(WorkDay.date.asc())
                .all()
            )

            if not row_collection:
                return None, ApiErrorData(
                    message=f"For this year: {year} and month: {month} is not available.",
                    type_module="collection_calendar_psql",
                    type_error="not_found",
                    key_type_error="NotFound",
                ), False

            days_data: list[CalendarDayResponse] = []
            weeks_data: dict[int, list[CalendarDayResponse]] = defaultdict(list)

            for work_day in row_collection:
                day_info = CalendarDayResponse(
                    id=str(work_day.id),
                    date=work_day.date,
                    day_number=work_day.date.day,
                    day_name=_DAY_NAMES[work_day.date.weekday()],
                    hours_worked=work_day.hours_worked or 0,
                    is_holiday=work_day.is_holiday,
                    norm_hours=work_day.norm_hours,
                    hourly_rate=work_day.hourly_rate,
                    daily_salary=(work_day.hours_worked or 0) * work_day.hourly_rate,
                )
                days_data.append(day_info)
                weeks_data[work_day.date.isocalendar()[1]].append(day_info)

            weeks_statistics: list[WeekStatisticsResponse] = []
            total_hours_month = 0
            total_norm_hours_month = 0
            total_salary_month = 0

            for week_num in sorted(weeks_data.keys()):
                week_days = weeks_data[week_num]
                week_hours = sum(day.hours_worked for day in week_days)
                week_norm_hours = sum(day.norm_hours for day in week_days)
                hourly_rate = week_days[0].hourly_rate if week_days else 0
                week_salary = week_hours * hourly_rate

                total_hours_month += week_hours
                total_norm_hours_month += week_norm_hours
                total_salary_month += week_salary

                weeks_statistics.append(
                    WeekStatisticsResponse(
                        week_number=week_num,
                        total_hours=week_hours,
                        total_norm_hours=week_norm_hours,
                        hourly_rate=hourly_rate,
                        salary=week_salary,
                    )
                )

            return CalendarCollectionResponse(
                year=year,
                month=month,
                month_name=_MONTH_NAMES.get(month, ""),
                days=days_data,
                statistics=MonthStatisticsResponse(
                    total_hours_worked=total_hours_month,
                    total_norm_hours=total_norm_hours_month,
                    total_salary=total_salary_month,
                    weeks=weeks_statistics,
                ),
            ), None, True

    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="collection_calendar_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
