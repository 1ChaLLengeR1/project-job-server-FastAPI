from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

MIN_YEAR = 2000


class CalendarCreatePayload(BaseModel):
    year: int = Field(description=f"Rok kalendarza (zakres: {MIN_YEAR} - bieżący rok + 10)")

    @field_validator("year")
    @classmethod
    def year_in_range(cls, value: int) -> int:
        max_year = datetime.now().year + 10
        if value < MIN_YEAR or value > max_year:
            raise ValueError(f"Year must be between {MIN_YEAR} and {max_year}")
        return value


class ConditionCreatePayload(BaseModel):
    norm_hours: float = Field(gt=0, description="Norma godzin dziennie")
    hourly_rate: float = Field(gt=0, description="Stawka godzinowa")


class ConditionUpdatePayload(ConditionCreatePayload):
    pass


class DayUpdateByIdPayload(BaseModel):
    norm_hours: float = Field(ge=0, le=24, description="Norma godzin (0-24)")
    hours_worked: float = Field(ge=0, le=24, description="Godziny przepracowane (0-24)")
    hourly_rate: float = Field(ge=0, description="Stawka godzinowa")


class DaysRangeUpdatePayload(BaseModel):
    year: int = Field(ge=1900, le=2100, description="Rok")
    month: int = Field(ge=1, le=12, description="Miesiąc")
    start_day: int = Field(ge=1, le=31, description="Dzień początkowy")
    end_day: int = Field(ge=1, le=31, description="Dzień końcowy")
    norm_hours: float = Field(ge=0, le=24, description="Norma godzin (0-24)")
    hours_worked: float = Field(ge=0, le=24, description="Godziny przepracowane (0-24)")
    hourly_rate: float = Field(ge=0, description="Stawka godzinowa")

    @model_validator(mode="after")
    def start_day_before_end_day(self) -> "DaysRangeUpdatePayload":
        if self.start_day > self.end_day:
            raise ValueError("Pole 'start_day' nie może być większe niż 'end_day'.")
        return self


class DaysSalaryUpdatePayload(BaseModel):
    year: int = Field(ge=1900, le=2100, description="Rok")
    month: int = Field(ge=1, le=12, description="Miesiąc")
    salary: float = Field(ge=0, description="Wypłata do rozbicia na stawkę godzinową")
