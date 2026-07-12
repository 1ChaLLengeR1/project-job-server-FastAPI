from datetime import datetime

from pydantic import BaseModel


class TaskResponseData(BaseModel):
    id: str
    description: str
    time: int
    active: bool
    created_at: datetime | None
    updated_at: datetime | None


class TaskStatisticsResponseData(BaseModel):
    total_tasks: int
    total_time: int
    average_per_week: float
    average_time_per_week: float
    tasks_per_day: dict[str, int]
