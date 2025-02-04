from consumer.data.response import ResponseData
from database.db import get_db
from database.logs.models import Logs


def collection_logs_psql(number: int):
    db_gen = get_db()
    db = next(db_gen)
    try:

        if number == 0:
            row_logs = db.query(Logs).order_by(Logs.date.desc()).all()
        else:
            row_logs = db.query(Logs).order_by(Logs.date.desc()).limit(number).all()

        logs = []
        for item in row_logs:
            logs.append(
                {
                    'id': str(item.id),
                    'username': item.username,
                    'description': item.description,
                    'date': item.date.isoformat(),
                }
            )

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=logs,
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
