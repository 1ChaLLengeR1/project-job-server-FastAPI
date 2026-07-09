from dataclasses import dataclass
from datetime import date

from database.psql.models.logs import Logs


@dataclass
class LogResponse:
    id: str
    username: str
    description: str
    date: date | None


def _to_log_response(model: Logs) -> LogResponse:
    return LogResponse(
        id=str(model.id),
        username=model.username,
        description=model.description,
        date=model.date,
    )
