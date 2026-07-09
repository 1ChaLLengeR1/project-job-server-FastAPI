"""Fabryki modeli domeny rentals — dane realne z docs/Obliczenia*.txt."""

from datetime import date
from uuid import uuid4

from sqlalchemy.orm import Session

from database.psql.models.rentals import (
    RentalAllocationRule,
    RentalApartment,
    RentalApartmentCost,
    RentalBeneficiary,
    RentalBeneficiarySettlement,
    RentalBeneficiarySettlementItem,
    RentalBillingPeriod,
    RentalCostType,
    RentalMeter,
    RentalMeterReading,
    RentalSettlement,
    RentalSettlementItem,
    RentalTenancy,
    RentalTenant,
)


def make_apartment(db: Session, *, name: str | None = None, is_active: bool = True) -> RentalApartment:
    apartment = RentalApartment(
        name=name or f"Pokój Państwa Dudzik {uuid4().hex[:8]}",
        description="parter, wejście od podwórka",
        is_active=is_active,
    )
    db.add(apartment)
    db.flush()
    return apartment


def make_tenant(
    db: Session, *, first_name: str | None = None, last_name: str | None = "Kydr", is_active: bool = True
) -> RentalTenant:
    tenant = RentalTenant(
        first_name=first_name or f"Łukasz {uuid4().hex[:8]}",
        last_name=last_name,
        is_active=is_active,
    )
    db.add(tenant)
    db.flush()
    return tenant


def make_tenancy(
    db: Session,
    *,
    apartment: RentalApartment | None = None,
    tenant: RentalTenant | None = None,
    rent_amount: float = 1000.00,
    persons_count: int = 1,
    start_date: date = date(2026, 1, 1),
    end_date: date | None = None,
) -> RentalTenancy:
    tenancy = RentalTenancy(
        apartment_id=(apartment or make_apartment(db)).id,
        tenant_id=(tenant or make_tenant(db)).id,
        rent_amount=rent_amount,
        persons_count=persons_count,
        start_date=start_date,
        end_date=end_date,
    )
    db.add(tenancy)
    db.flush()
    return tenancy


def make_cost_type(
    db: Session, *, name: str | None = None, charge_type: str = "fixed", is_active: bool = True
) -> RentalCostType:
    cost_type = RentalCostType(
        name=name or f"internet {uuid4().hex[:8]}",
        charge_type=charge_type,
        is_active=is_active,
    )
    db.add(cost_type)
    db.flush()
    return cost_type


def make_apartment_cost(
    db: Session,
    *,
    apartment: RentalApartment | None = None,
    cost_type: RentalCostType | None = None,
    amount: float = 60.00,
    start_date: date = date(2026, 1, 1),
    end_date: date | None = None,
) -> RentalApartmentCost:
    apartment_cost = RentalApartmentCost(
        apartment_id=(apartment or make_apartment(db)).id,
        cost_type_id=(cost_type or make_cost_type(db)).id,
        amount=amount,
        start_date=start_date,
        end_date=end_date,
    )
    db.add(apartment_cost)
    db.flush()
    return apartment_cost


def make_meter(
    db: Session,
    *,
    apartment: RentalApartment | None = None,
    apartment_id=None,
    media_type: str = "electricity",
    is_master: bool = False,
    is_active: bool = True,
) -> RentalMeter:
    if apartment_id is None and apartment is not None:
        apartment_id = apartment.id
    meter = RentalMeter(
        apartment_id=apartment_id,
        media_type=media_type,
        is_master=is_master,
        name=f"licznik {media_type} {uuid4().hex[:8]}",
        is_active=is_active,
    )
    db.add(meter)
    db.flush()
    return meter


def make_billing_period(
    db: Session,
    *,
    period_month: date = date(2026, 6, 1),
    status: str = "draft",
    electricity_bill_amount: float | None = 899.48,
    electricity_rate: float | None = 1.05,
    water_rate: float = 9.00,
) -> RentalBillingPeriod:
    period = RentalBillingPeriod(
        period_month=period_month,
        status=status,
        electricity_bill_amount=electricity_bill_amount,
        electricity_rate=electricity_rate,
        water_rate=water_rate,
    )
    db.add(period)
    db.flush()
    return period


def make_meter_reading(
    db: Session,
    *,
    period: RentalBillingPeriod | None = None,
    meter: RentalMeter | None = None,
    previous_value: float = 5621.26,
    current_value: float = 5938.86,
    error_correction: float = 0,
) -> RentalMeterReading:
    reading = RentalMeterReading(
        period_id=(period or make_billing_period(db)).id,
        meter_id=(meter or make_meter(db)).id,
        previous_value=previous_value,
        current_value=current_value,
        error_correction=error_correction,
    )
    db.add(reading)
    db.flush()
    return reading


def make_settlement(
    db: Session,
    *,
    period: RentalBillingPeriod | None = None,
    apartment: RentalApartment | None = None,
    tenancy: RentalTenancy | None = None,
    rent_amount: float = 1100.00,
    electricity_cost: float = 335.00,
    water_cost: float = 64.00,
    total_media_amount: float = 529.00,
    total_amount: float = 1629.00,
) -> RentalSettlement:
    settlement = RentalSettlement(
        period_id=(period or make_billing_period(db)).id,
        apartment_id=(apartment or make_apartment(db)).id,
        tenancy_id=tenancy.id if tenancy else None,
        rent_amount=rent_amount,
        electricity_consumption=318.6,
        electricity_cost=electricity_cost,
        water_consumption=7.125,
        water_cost=water_cost,
        total_media_amount=total_media_amount,
        total_amount=total_amount,
    )
    db.add(settlement)
    db.flush()
    return settlement


def make_settlement_item(
    db: Session,
    *,
    settlement: RentalSettlement | None = None,
    cost_type: RentalCostType | None = None,
    name: str = "śmieci (2 os. x 35 zł)",
    kind: str = "fixed_cost",
    amount: float = 70.00,
) -> RentalSettlementItem:
    item = RentalSettlementItem(
        settlement_id=(settlement or make_settlement(db)).id,
        cost_type_id=cost_type.id if cost_type else None,
        name=name,
        kind=kind,
        amount=amount,
    )
    db.add(item)
    db.flush()
    return item


def make_beneficiary(db: Session, *, name: str | None = None, is_active: bool = True) -> RentalBeneficiary:
    beneficiary = RentalBeneficiary(name=name or f"Ojciec {uuid4().hex[:8]}", is_active=is_active)
    db.add(beneficiary)
    db.flush()
    return beneficiary


def make_allocation_rule(
    db: Session,
    *,
    beneficiary: RentalBeneficiary | None = None,
    apartment: RentalApartment | None = None,
    cost_type: RentalCostType | None = None,
    component: str = "rent",
    mode: str = "fixed_amount",
    amount: float | None = 1100.00,
    description: str | None = None,
    start_date: date = date(2026, 1, 1),
    end_date: date | None = None,
) -> RentalAllocationRule:
    rule = RentalAllocationRule(
        beneficiary_id=(beneficiary or make_beneficiary(db)).id,
        apartment_id=apartment.id if apartment else None,
        cost_type_id=cost_type.id if cost_type else None,
        component=component,
        mode=mode,
        amount=amount,
        description=description,
        start_date=start_date,
        end_date=end_date,
    )
    db.add(rule)
    db.flush()
    return rule


def make_beneficiary_settlement(
    db: Session,
    *,
    period: RentalBillingPeriod | None = None,
    beneficiary: RentalBeneficiary | None = None,
    total_amount: float = 1790.00,
) -> RentalBeneficiarySettlement:
    settlement = RentalBeneficiarySettlement(
        period_id=(period or make_billing_period(db)).id,
        beneficiary_id=(beneficiary or make_beneficiary(db)).id,
        total_amount=total_amount,
    )
    db.add(settlement)
    db.flush()
    return settlement


def make_beneficiary_settlement_item(
    db: Session,
    *,
    beneficiary_settlement: RentalBeneficiarySettlement | None = None,
    description: str = "czynsz - Pokój Państwa Dudzik",
    amount: float = 1100.00,
) -> RentalBeneficiarySettlementItem:
    item = RentalBeneficiarySettlementItem(
        beneficiary_settlement_id=(beneficiary_settlement or make_beneficiary_settlement(db)).id,
        description=description,
        amount=amount,
    )
    db.add(item)
    db.flush()
    return item
