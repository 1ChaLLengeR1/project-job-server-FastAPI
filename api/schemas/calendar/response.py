from datetime import date, datetime

from pydantic import BaseModel


class GeneratedDayData(BaseModel):
    date: date
    hours_worked: float | None
    is_holiday: bool
    is_weekend: bool
    norm_hours: float
    hourly_rate: float


class GeneratedCalendarSummaryData(BaseModel):
    total_days: int
    total_holidays: int
    total_weekends: int
    year: int
    days_before_today: int
    working_days: int


class GeneratedCalendarData(BaseModel):
    calendar_days: list[GeneratedDayData]
    inserted_count: int
    summary: GeneratedCalendarSummaryData


class CalendarDayData(BaseModel):
    id: str
    date: date
    day_number: int
    day_name: str
    hours_worked: float
    is_holiday: bool
    norm_hours: float
    hourly_rate: float
    daily_salary: float


class WeekStatisticsData(BaseModel):
    week_number: int
    total_hours: float
    total_norm_hours: float
    hourly_rate: float
    salary: float


class MonthStatisticsData(BaseModel):
    total_hours_worked: float
    total_norm_hours: float
    total_salary: float
    weeks: list[WeekStatisticsData]


class CalendarCollectionData(BaseModel):
    year: int
    month: int
    month_name: str
    days: list[CalendarDayData]
    statistics: MonthStatisticsData


class CalendarStatisticsData(BaseModel):
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


class WorkConditionData(BaseModel):
    id: str
    start_date: date
    norm_hours: float
    hourly_rate: float
    created_at: datetime | None
    updated_at: datetime | None


class WorkDayUpdateData(BaseModel):
    id: str
    date: date
    norm_hours: float
    hours_worked: float | None
    hourly_rate: float
    updated_at: datetime | None


class WorkDaysRangeUpdateData(BaseModel):
    updated_count: int
    start_date: date
    end_date: date
    days: list[date]


class SalaryUpdatedDayData(BaseModel):
    id: str
    date: date
    hours_worked: float
    hourly_rate: float
    daily_salary: float


class SalaryUpdateData(BaseModel):
    updated_count: int
    total_hours_worked: float
    calculated_hourly_rate: float
    expected_salary: float
    actual_total_salary: float
    updated_days: list[SalaryUpdatedDayData]
