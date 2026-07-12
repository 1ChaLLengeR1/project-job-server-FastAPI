from datetime import date

from sqlalchemy.orm import Session

from api.response import ApiErrorData
from core.repository.psql.logs.create import create_logs_psql
from core.repository.psql.rental.billing.create import (
    create_billing_period_psql,
    create_meter_reading_psql,
)
from core.repository.psql.rental.billing.one import one_last_meter_reading_psql
from core.repository.psql.rental.billing.response import BillingPeriodResponse, MeterReadingResponse
from core.repository.psql.rental.dictionaries.collection import collection_meters_psql


def handler_create_billing_period(
    user_id: str,
    period_month: date,
    electricity_bill_amount: float | None = None,
    electricity_rate: float | None = None,
    electricity_rate_is_manual: bool = False,
    water_rate: float = 9.00,
    note: str | None = None,
    db_session: Session | None = None,
) -> tuple[BillingPeriodResponse | None, ApiErrorData | None, bool]:
    """Nowy okres + szkielet odczytów dla aktywnych liczników.

    Prefill: "Ostatnio" = "Teraz" z ostatniego okresu danego licznika (0 dla nowego licznika);
    "Teraz" startuje z tą samą wartością — user uzupełnia faktyczne odczyty.
    """
    try:
        period, err, ok = create_billing_period_psql(
            period_month,
            electricity_bill_amount,
            electricity_rate,
            electricity_rate_is_manual,
            water_rate,
            note,
            db_session=db_session,
        )
        if not ok:
            return None, err, False

        meters, err, ok = collection_meters_psql(is_active=True, db_session=db_session)
        if not ok:
            return None, err, False

        for meter in meters:
            last_reading, _, last_ok = one_last_meter_reading_psql(meter.id, db_session=db_session)
            previous_value = last_reading.current_value if last_ok else 0
            _, err, ok = create_meter_reading_psql(
                period.id, meter.id, previous_value, previous_value, 0, db_session=db_session
            )
            if not ok:
                return None, err, False

        create_logs_psql(user_id, "rental:create_billing_period", db_session=db_session)
        return period, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_create_billing_period",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )


def handler_create_meter_reading(
    user_id: str,
    period_id: str,
    meter_id: str,
    previous_value: float,
    current_value: float,
    error_correction: float = 0,
    db_session: Session | None = None,
) -> tuple[MeterReadingResponse | None, ApiErrorData | None, bool]:
    """Ręczne dodanie odczytu — np. licznik założony po utworzeniu okresu."""
    try:
        result, err, ok = create_meter_reading_psql(
            period_id, meter_id, previous_value, current_value, error_correction, db_session=db_session
        )
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "rental:create_meter_reading", db_session=db_session)
        return result, None, True
    except Exception as e:
        return (
            None,
            ApiErrorData(
                message=str(e),
                type_module="handler_create_meter_reading",
                type_error="exception",
                key_type_error="Exception",
            ),
            False,
        )
