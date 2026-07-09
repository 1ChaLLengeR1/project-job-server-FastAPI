from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.rental.billing.response import (
    BillingPeriodResponse,
    MeterReadingResponse,
    SettlementResponse,
    _to_billing_period_response,
    _to_meter_reading_response,
    _to_settlement_response,
)
from database.psql.database import managed_session
from database.psql.models.rentals import (
    RentalBillingPeriod,
    RentalMeterReading,
    RentalSettlement,
    RentalSettlementItem,
)


def collection_billing_periods_psql(
    status: str | None = None, db_session: Session | None = None
) -> tuple[list[BillingPeriodResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(RentalBillingPeriod)
            if status is not None:
                query = query.filter(RentalBillingPeriod.status == status)
            periods = query.order_by(RentalBillingPeriod.period_month.desc()).all()
            return [_to_billing_period_response(period) for period in periods], None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_billing_periods_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def collection_meter_readings_psql(
    period_id: str, db_session: Session | None = None
) -> tuple[list[MeterReadingResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            readings = (
                db.query(RentalMeterReading)
                .filter(RentalMeterReading.period_id == period_id)
                .order_by(RentalMeterReading.created_at.asc())
                .all()
            )
            return [_to_meter_reading_response(reading) for reading in readings], None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_meter_readings_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def collection_settlements_psql(
    period_id: str | None = None,
    apartment_id: str | None = None,
    db_session: Session | None = None,
) -> tuple[list[SettlementResponse] | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            query = db.query(RentalSettlement)
            if period_id is not None:
                query = query.filter(RentalSettlement.period_id == period_id)
            if apartment_id is not None:
                query = query.filter(RentalSettlement.apartment_id == apartment_id)
            settlements = query.order_by(RentalSettlement.created_at.asc()).all()

            settlement_ids = [settlement.id for settlement in settlements]
            items_by_settlement: dict = {}
            if settlement_ids:
                items = (
                    db.query(RentalSettlementItem)
                    .filter(RentalSettlementItem.settlement_id.in_(settlement_ids))
                    .order_by(RentalSettlementItem.created_at.asc())
                    .all()
                )
                for item in items:
                    items_by_settlement.setdefault(item.settlement_id, []).append(item)

            return (
                [
                    _to_settlement_response(settlement, items_by_settlement.get(settlement.id, []))
                    for settlement in settlements
                ],
                None,
                True,
            )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="collection_settlements_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
