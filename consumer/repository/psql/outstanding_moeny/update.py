from consumer.data.response import ResponseData
from database.db import get_db
from consumer.data.user import UserData
from database.outstanding_money.models import NamesOverdue, OutStandingMoney
from consumer.repository.psql.user.check import check_user_role_psql
from consumer.data.outstanding_moeny.update import EditListParams, EditItem


def edit_name_list_psql(user_data: UserData, payload: EditListParams) -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:
        check_role = check_user_role_psql(user_data, 'superadmin')
        if not check_role['is_valid']:
            return ResponseData(
                is_valid=check_role['is_valid'],
                status=check_role['status'],
                data=check_role['data'],
                status_code=check_role['status_code'],
                additional=check_role['additional']
            )

        item_row = db.query(NamesOverdue).filter(NamesOverdue.id == payload['id']).first()
        if not item_row:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=str(f"Not found item with this id: {payload['id']}"),
                status_code=400,
                additional=None
            )

        item_row.name = payload['name']
        db.commit()

        data = {
            "id": str(item_row.id),
            "name": item_row.name
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


def edit_item_psql(user_data: UserData, payload: EditItem) -> ResponseData:
    db_gen = get_db()
    db = next(db_gen)
    try:
        check_role = check_user_role_psql(user_data, 'superadmin')
        if not check_role['is_valid']:
            return ResponseData(
                is_valid=check_role['is_valid'],
                status=check_role['status'],
                data=check_role['data'],
                status_code=check_role['status_code'],
                additional=check_role['additional']
            )

        edit_item = db.query(OutStandingMoney).filter(OutStandingMoney.id == payload['id']).first()
        if not edit_item:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=str(f"Not found edit_item with this id: {payload['id']}"),
                status_code=400,
                additional=None
            )

        edit_item.amount = payload['amount']
        edit_item.name = payload['name']

        db.commit()

        data = {
            'id': str(edit_item.id),
            'amount': edit_item.amount,
            'name': edit_item.name,
            'date': edit_item.date.isoformat(),
            'id_name': str(edit_item.id_name)
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
