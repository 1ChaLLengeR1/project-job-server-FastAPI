from consumer.data.response import ResponseData
from database.db import get_db
from consumer.data.user import UserData
from database.outstanding_money.models import NamesOverdue, OutStandingMoney
from consumer.repository.psql.user.check import check_user_role_psql


def delete_list_psql(user_data: UserData, id: str) -> ResponseData:
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

        item_names_overdue = db.query(NamesOverdue).filter(NamesOverdue.id == id).first()
        if not item_names_overdue:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=f"Not found item_names_overdue with this id: {id}",
                status_code=400,
                additional=None
            )

        item_outstanding_money = db.query(OutStandingMoney).filter(OutStandingMoney.id_name == id).all()
        if not item_outstanding_money:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=f"Not found item_outstanding_money with this id_name: {id}",
                status_code=400,
                additional=None
            )

        db.delete(item_names_overdue)
        for item in item_outstanding_money:
            db.delete(item)

        db.commit()

        data = {
            'name_overdue': {
                'id': item_names_overdue.id,
                'name': item_names_overdue.name
            },
            'outstanding_money': [
                {
                    'id': item.id,
                    'amount': item.amount,
                    'name': item.name,
                    'date': item.date,
                    'id_name': item.id_name
                }
                for item in item_outstanding_money
            ]
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


def delete_item_psql(user_data: UserData, id: str) -> ResponseData:
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

        row_out_standing_money = db.query(OutStandingMoney).filter(OutStandingMoney.id == id).first()
        if not row_out_standing_money:
            return ResponseData(
                is_valid=False,
                status="ERROR",
                data=f"Not found out_standing_money with this id_name: {id}",
                status_code=400,
                additional=None
            )

        deleted_item_data = {
            "id": row_out_standing_money.id,
            "amount": row_out_standing_money.amount,
            "name": row_out_standing_money.name,
            "date": row_out_standing_money.date.isoformat(),
            "id_name": row_out_standing_money.id_name
        }

        db.delete(row_out_standing_money)
        db.commit()

        return ResponseData(
            is_valid=True,
            status="SUCCESS",
            data=deleted_item_data,
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
