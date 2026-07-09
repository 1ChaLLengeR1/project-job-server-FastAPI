from dataclasses import dataclass
from datetime import date


@dataclass
class GeneratedDayResponse:
    date: date
    hours_worked: float | None
    is_holiday: bool
    is_weekend: bool
    norm_hours: float
    hourly_rate: float


@dataclass
class GeneratedCalendarSummaryResponse:
    total_days: int
    total_holidays: int
    total_weekends: int
    year: int
    days_before_today: int
    working_days: int


@dataclass
class GeneratedCalendarResponse:
    calendar_days: list[GeneratedDayResponse]
    inserted_count: int
    summary: GeneratedCalendarSummaryResponse


@dataclass
class CalendarDayResponse:
    id: str
    date: date
    day_number: int
    day_name: str
    hours_worked: float
    is_holiday: bool
    norm_hours: float
    hourly_rate: float
    daily_salary: float


@dataclass
class WeekStatisticsResponse:
    week_number: int
    total_hours: float
    total_norm_hours: float
    hourly_rate: float
    salary: float


@dataclass
class MonthStatisticsResponse:
    total_hours_worked: float
    total_norm_hours: float
    total_salary: float
    weeks: list[WeekStatisticsResponse]


@dataclass
class CalendarCollectionResponse:
    year: int
    month: int
    month_name: str
    days: list[CalendarDayResponse]
    statistics: MonthStatisticsResponse


@dataclass
class CalendarStatisticsResponse:
    year: int
    total_hours_worked: float
    total_earnings: float
    working_days_count: int
    total_norm_hours: float
    hours_difference: float
    total_holidays: int
    total_days_in_year: int
    average_hours_per_working_day: float
    average_daily_earnings: float
    work_efficiency_percentage: float
