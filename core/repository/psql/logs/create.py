from core.data.response import ResponseData
from database.db import get_db
from database.logs.models import Logs
from core.data.user import UserData
import datetime


def create_logs_psql(user_data: UserData, description: str):
    db_gen = get_db()
    db = next(db_gen)
    try:

        new_log = Logs(username=user_data['username'], description=description, date=datetime.datetime.now())
        db.add(new_log)
        db.commit()

        data = {
            'id': str(new_log.id),
            'username': new_log.username,
            'description': new_log.description,
            'date': new_log.date.isoformat()
        }

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=data,
            status_code=200,
            additional=None
        )

    except Exception as e:
        return ResponseData(
            is_valid=False,
            status="ERROR",
            data=str(e),
            status_code=417,
            additional=None
        )
    finally:
        db.close()
