from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class WorkDayUpdateResponse:
    id: str
    date: date
    norm_hours: float
    hours_worked: float | None
    hourly_rate: float
    updated_at: datetime | None


@dataclass
class WorkDaysRangeUpdateResponse:
    updated_count: int
    start_date: date
    end_date: date
    days: list[date]


@dataclass
class AutoUpdatedDayResponse:
    id: str
    date: date
    norm_hours: float
    hours_worked: float | None
    hourly_rate: float


@dataclass
class ConditionUsedResponse:
    norm_hours: float
    hourly_rate: float
    start_date: date


@dataclass
class AutoUpdateDaysResponse:
    updated_count: int
    updated_days: list[AutoUpdatedDayResponse]
    condition_used: ConditionUsedResponse


@dataclass
class SalaryUpdatedDayResponse:
    id: str
    date: date
    hours_worked: float
    hourly_rate: float
    daily_salary: float


@dataclass
class SalaryUpdateResponse:
    updated_count: int
    total_hours_worked: float
    calculated_hourly_rate: float
    expected_salary: float
    actual_total_salary: float
    updated_days: list[SalaryUpdatedDayResponse]
