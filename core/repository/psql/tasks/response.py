from dataclasses import dataclass
from datetime import datetime

from database.psql.models.tasks import Tasks


@dataclass
class TaskResponse:
    id: str
    description: str
    time: int
    active: bool
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class TaskStatisticsResponse:
    total_tasks: int
    total_time: int
    average_per_week: float
    average_time_per_week: float
    tasks_per_day: dict[str, int]


def _to_task_response(model: Tasks) -> TaskResponse:
    return TaskResponse(
        id=str(model.id),
        description=model.description,
        time=model.time,
        active=model.active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
