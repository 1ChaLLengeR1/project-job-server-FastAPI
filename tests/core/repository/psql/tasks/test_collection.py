from sqlalchemy.orm import Session

from core.repository.psql.tasks.collection import collection_tasks_psql
from tests.core.repository.psql.tasks.helper import make_task


class TestCollectionTasksPsql:
    def test_collection01_filters_by_active(self, db_session: Session):
        make_task(db_session, description="aktywny", active=True)
        make_task(db_session, description="wykonany", active=False)

        result, err, ok = collection_tasks_psql(True, db_session=db_session)

        assert ok is True and err is None
        assert [task.description for task in result] == ["aktywny"]

    def test_collection02_inactive_only(self, db_session: Session):
        make_task(db_session, active=True)
        make_task(db_session, description="wykonany", active=False)

        result, err, ok = collection_tasks_psql(False, db_session=db_session)

        assert ok is True
        assert [task.description for task in result] == ["wykonany"]

    def test_collection03_empty_returns_empty_list(self, db_session: Session):
        result, err, ok = collection_tasks_psql(True, db_session=db_session)

        assert ok is True and result == []
