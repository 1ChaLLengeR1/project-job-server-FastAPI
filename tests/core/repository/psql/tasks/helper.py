from uuid import uuid4

from sqlalchemy.orm import Session

from database.psql.models.tasks import Tasks


def make_task(
    db: Session,
    *,
    description: str | None = None,
    time: int = 30,
    active: bool = True,
) -> Tasks:
    task = Tasks(description=description or f"task_{uuid4().hex[:8]}", time=time, active=active)
    db.add(task)
    db.flush()
    return task
