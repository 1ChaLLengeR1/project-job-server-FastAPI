from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from database.psql.models.logs import Logs


def make_log(
    db: Session,
    *,
    username: str | None = None,
    description: str = "tasks:create",
    date: datetime | None = None,
) -> Logs:
    log = Logs(
        username=username or f"user_{uuid4().hex[:8]}",
        description=description,
        date=date or datetime.now(timezone.utc),
    )
    db.add(log)
    db.flush()
    return log
