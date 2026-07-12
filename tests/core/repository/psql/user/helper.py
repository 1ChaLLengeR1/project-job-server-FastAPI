from uuid import uuid4

from sqlalchemy.orm import Session

from database.psql.models.auth import Users


def create_test_user(
    db: Session,
    *,
    username: str | None = None,
    password: str = "$2b$12$fakehashfakehashfakehashfakehashfakehashfakehashfak",
    type: str = "user",
) -> Users:
    user = Users(username=username or f"user_{uuid4().hex[:8]}", password=password, type=type)
    db.add(user)
    db.flush()
    return user
