from dataclasses import dataclass
from datetime import date, datetime

from database.psql.models.calendar import WorkConditionChange


@dataclass
class WorkConditionResponse:
    id: str
    start_date: date
    norm_hours: float
    hourly_rate: float
    created_at: datetime | None
    updated_at: datetime | None


def _to_work_condition_response(model: WorkConditionChange) -> WorkConditionResponse:
    return WorkConditionResponse(
        id=str(model.id),
        start_date=model.start_date,
        norm_hours=model.norm_hours,
        hourly_rate=model.hourly_rate,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )
