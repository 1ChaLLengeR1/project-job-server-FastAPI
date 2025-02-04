from consumer.data.response import ResponseData
from database.db import get_db
from sqlalchemy import desc
from database.outstanding_money.models import NamesOverdue, OutStandingMoney


def collection_list_psql() -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:
        list_overdue = []
        item_names_overdue = db.query(NamesOverdue).all()

        for item in item_names_overdue:
            object_item = {
                "id_name": str(item.id),
                "name_overdue": item.name,
                "array_items": [],
                "full_price": 0
            }

            item_outstanding_money = db.query(OutStandingMoney).filter(OutStandingMoney.id_name == str(item.id)).order_by(
                desc(OutStandingMoney.date)).all()
            for items in item_outstanding_money:
                object_items = {
                    "id": str(items.id),
                    "amount": items.amount,
                    "name": items.name,
                    "date": items.date.isoformat(),
                }
                object_item['array_items'].append(object_items)
                object_item['full_price'] += items.amount

            list_overdue.append(object_item)

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=list_overdue,
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
