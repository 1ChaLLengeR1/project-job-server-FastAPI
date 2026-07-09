from sqlalchemy import desc
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.outstanding_money.response import (
    OverdueListResponse,
    _to_outstanding_item_response,
)
from database.psql.database import managed_session
from database.psql.models.outstanding_money import NamesOverdue, OutStandingMoney


def collection_list_psql(
    db_session: Session | None = None,
) -> tuple[list[OverdueListResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            list_overdue: list[OverdueListResponse] = []

            for item in db.query(NamesOverdue).all():
                items = (
                    db.query(OutStandingMoney)
                    .filter(OutStandingMoney.id_name == item.id)
                    .order_by(desc(OutStandingMoney.date))
                    .all()
                )
                array_items = [_to_outstanding_item_response(row) for row in items]

                list_overdue.append(
                    OverdueListResponse(
                        id_name=str(item.id),
                        name_overdue=item.name,
                        array_items=array_items,
                        full_price=sum(row.amount for row in array_items),
                    )
                )

            return list_overdue, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="collection_list_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
