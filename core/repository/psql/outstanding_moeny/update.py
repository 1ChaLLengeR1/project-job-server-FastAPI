from core.data.outstanding_moeny.update import EditItem, EditListParams
from core.data.response import ResponseData
from database.psql.database import get_db
from database.psql.models.outstanding_money import NamesOverdue, OutStandingMoney


def edit_name_list_psql(payload: EditListParams) -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:
        item_row = db.query(NamesOverdue).filter(NamesOverdue.id == payload["id"]).first()
        if not item_row:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=str(f"Not found item with this id: {payload['id']}"),
                status_code=400,
                additional=None,
            )

        item_row.name = payload["name"]
        db.commit()

        data = {"id": str(item_row.id), "name": item_row.name}

        return ResponseData(is_valid=True, status="SUCCESS", data=data, status_code=200, additional=None)

    except Exception as e:
        return ResponseData(is_valid=False, status="ERROR", data=str(e), status_code=417, additional=None)
    finally:
        db.close()


def edit_item_psql(payload: EditItem) -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:
        edit_item = db.query(OutStandingMoney).filter(OutStandingMoney.id == payload["id"]).first()
        if not edit_item:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=str(f"Not found edit_item with this id: {payload['id']}"),
                status_code=400,
                additional=None,
            )

        edit_item.amount = payload["amount"]
        edit_item.name = payload["name"]

        db.commit()

        data = {
            "id": str(edit_item.id),
            "amount": edit_item.amount,
            "name": edit_item.name,
            "date": edit_item.date.isoformat(),
            "id_name": str(edit_item.id_name),
        }

        return ResponseData(is_valid=True, status="SUCCESS", data=data, status_code=200, additional=None)

    except Exception as e:
        return ResponseData(is_valid=False, status="ERROR", data=str(e), status_code=417, additional=None)
    finally:
        db.close()
