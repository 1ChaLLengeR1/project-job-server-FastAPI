from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.rental.billing.response import (
    BillingPeriodResponse,
    MeterReadingResponse,
    _to_billing_period_response,
    _to_meter_reading_response,
)
from database.psql.database import managed_session
from database.psql.models.rentals import (
    RentalBeneficiarySettlement,
    RentalBeneficiarySettlementItem,
    RentalBillingPeriod,
    RentalMeterReading,
    RentalSettlement,
    RentalSettlementItem,
)


def _delete_period_snapshots(db: Session, period_id: str) -> int:
    """Usuwa snapshoty okresu (rozliczenia mieszkań + podział rodzinny). Zwraca liczbę rozliczeń."""
    beneficiary_settlement_ids = [
        row.id
        for row in db.query(RentalBeneficiarySettlement)
        .filter(RentalBeneficiarySettlement.period_id == period_id)
        .all()
    ]
    if beneficiary_settlement_ids:
        db.query(RentalBeneficiarySettlementItem).filter(
            RentalBeneficiarySettlementItem.beneficiary_settlement_id.in_(beneficiary_settlement_ids)
        ).delete(synchronize_session=False)
    db.query(RentalBeneficiarySettlement).filter(RentalBeneficiarySettlement.period_id == period_id).delete(
        synchronize_session=False
    )

    settlement_ids = [
        row.id for row in db.query(RentalSettlement).filter(RentalSettlement.period_id == period_id).all()
    ]
    if settlement_ids:
        db.query(RentalBeneficiarySettlementItem).filter(
            RentalBeneficiarySettlementItem.settlement_id.in_(settlement_ids)
        ).delete(synchronize_session=False)
        db.query(RentalSettlementItem).filter(RentalSettlementItem.settlement_id.in_(settlement_ids)).delete(
            synchronize_session=False
        )
    deleted_settlements = (
        db.query(RentalSettlement).filter(RentalSettlement.period_id == period_id).delete(synchronize_session=False)
    )
    return deleted_settlements


def delete_billing_period_psql(
    period_id: str, db_session: Session | None = None
) -> tuple[BillingPeriodResponse | None, ApiErrorData | None, bool]:
    """Usuwa okres wraz z odczytami i snapshotami rozliczeń (pełne wycofanie błędnie założonego okresu)."""
    try:
        with managed_session(db_session) as (db, _):
            period = db.query(RentalBillingPeriod).filter(RentalBillingPeriod.id == period_id).first()
            if not period:
                return (
                    None,
                    ApiErrorData(
                        message="Okres rozliczeniowy nie istnieje",
                        type_module="delete_billing_period_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            deleted_period = _to_billing_period_response(period)
            _delete_period_snapshots(db, period_id)
            db.query(RentalMeterReading).filter(RentalMeterReading.period_id == period_id).delete(
                synchronize_session=False
            )
            db.delete(period)
            db.flush()
            return deleted_period, None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="delete_billing_period_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="delete_billing_period_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def delete_meter_reading_psql(
    reading_id: str, db_session: Session | None = None
) -> tuple[MeterReadingResponse | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            reading = db.query(RentalMeterReading).filter(RentalMeterReading.id == reading_id).first()
            if not reading:
                return (
                    None,
                    ApiErrorData(
                        message="Odczyt licznika nie istnieje",
                        type_module="delete_meter_reading_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            deleted_reading = _to_meter_reading_response(reading)
            db.delete(reading)
            db.flush()
            return deleted_reading, None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="delete_meter_reading_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="delete_meter_reading_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def delete_settlements_by_period_psql(
    period_id: str, db_session: Session | None = None
) -> tuple[int | None, ApiErrorData | None, bool]:
    """Usuwa snapshoty rozliczeń okresu (mieszkania + podział rodzinny) — używane przy reopen okresu."""
    try:
        with managed_session(db_session) as (db, _):
            period = db.query(RentalBillingPeriod).filter(RentalBillingPeriod.id == period_id).first()
            if not period:
                return (
                    None,
                    ApiErrorData(
                        message="Okres rozliczeniowy nie istnieje",
                        type_module="delete_settlements_by_period_psql",
                        type_error="not_found",
                        key_type_error="NotFound",
                    ),
                    False,
                )

            deleted_settlements = _delete_period_snapshots(db, period_id)
            db.flush()
            return deleted_settlements, None, True
    except IntegrityError as e:
        return (
            None,
            ApiErrorData(
                message=str(e.orig),
                type_module="delete_settlements_by_period_psql",
                type_error="integrity_error",
                key_type_error="IntegrityError",
            ),
            False,
        )
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="delete_settlements_by_period_psql",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
