from core.data.response import ResponseData
from database.db import get_db
import uuid
from uuid import UUID
from datetime import datetime
from database.outstanding_money.models import NamesOverdue, OutStandingMoney
from core.repository.psql.user.check import check_user_role_psql
from core.data.outstanding_moeny.create import CreateListParams, AddItemParams
from core.data.user import UserData


def create_list_psql(user_data: UserData, payload: CreateListParams) -> ResponseData:
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

        new_uuid4 = uuid.uuid4()
        new_outstanding_money_list = []

        new_names_overdue = NamesOverdue(id=new_uuid4, name=payload['name'])
        db.add(new_names_overdue)

        for item in payload['array_object']:
            new_outstanding_money = OutStandingMoney(amount=item['amount'], name=item['name'], date=datetime.now(),
                                                     id_name=new_uuid4)
            db.add(new_outstanding_money)
            new_outstanding_money_list.append({
                "amount": new_outstanding_money.amount,
                "name": new_outstanding_money.name,
                "date": new_outstanding_money.date.isoformat(),
                "id_name": str(new_outstanding_money.id_name)
            })

        db.commit()

        data = {
            "names_overdue": {
                "id": str(new_uuid4),
                "name": payload['name']
            },
            "new_outstanding_money": new_outstanding_money_list
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


def add_item_psql(user_data: UserData, payload: AddItemParams) -> ResponseData:
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

        id_name_uuid = UUID(payload['id_name'])
        row_item = db.query(NamesOverdue).filter(NamesOverdue.id == payload['id_name']).first()
        if not row_item:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=str(f"Not found item with this id_name: {payload['id_name']}"),
                status_code=400,
                additional=None,
            )

        new_item = OutStandingMoney(amount=payload['amount'], name=payload['name'], date=datetime.now(),
                                    id_name=id_name_uuid)
        db.add(new_item)
        db.commit()

        data = {
            'id': str(new_item.id),
            'amount': new_item.amount,
            'name': new_item.name,
            'date': new_item.date.isoformat(),
            'id_name': str(new_item.id_name)
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
