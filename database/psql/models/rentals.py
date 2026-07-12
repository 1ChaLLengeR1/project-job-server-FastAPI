import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.psql.base import Base

# ---------------------------------------------------------------------------
# Słowniki i konfiguracja
# ---------------------------------------------------------------------------


class RentalApartment(Base):
    __tablename__ = "rentals_apartments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # passive_deletes=True: nie nulluj/nie kasuj dzieci z ORM — o usunięciu decyduje baza (RESTRICT)
    tenancies = relationship("RentalTenancy", back_populates="apartment", passive_deletes=True)
    costs = relationship("RentalApartmentCost", back_populates="apartment", passive_deletes=True)
    meters = relationship("RentalMeter", back_populates="apartment", passive_deletes=True)
    settlements = relationship("RentalSettlement", back_populates="apartment", passive_deletes=True)
    allocation_rules = relationship("RentalAllocationRule", back_populates="apartment", passive_deletes=True)


class RentalTenant(Base):
    __tablename__ = "rentals_tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    note = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tenancies = relationship("RentalTenancy", back_populates="tenant", passive_deletes=True)


class RentalTenancy(Base):
    __tablename__ = "rentals_tenancies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apartment_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_apartments.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    tenant_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_tenants.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    rent_amount = Column(Numeric(10, 2), nullable=False)
    persons_count = Column(Integer, default=1, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # NULL = najem trwa
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    apartment = relationship("RentalApartment", back_populates="tenancies")
    tenant = relationship("RentalTenant", back_populates="tenancies")
    settlements = relationship("RentalSettlement", back_populates="tenancy", passive_deletes=True)


class RentalCostType(Base):
    __tablename__ = "rentals_cost_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    charge_type = Column(String(50), nullable=False)  # fixed | per_person
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    apartment_costs = relationship("RentalApartmentCost", back_populates="cost_type", passive_deletes=True)
    settlement_items = relationship("RentalSettlementItem", back_populates="cost_type", passive_deletes=True)
    allocation_rules = relationship("RentalAllocationRule", back_populates="cost_type", passive_deletes=True)


class RentalApartmentCost(Base):
    __tablename__ = "rentals_apartment_costs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apartment_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_apartments.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    cost_type_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_cost_types.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    amount = Column(Numeric(10, 2), nullable=False)  # dla per_person: stawka za osobę
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    apartment = relationship("RentalApartment", back_populates="costs")
    cost_type = relationship("RentalCostType", back_populates="apartment_costs")


class RentalMeter(Base):
    __tablename__ = "rentals_meters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # NULL = licznik główny budynku (nieprzypisany do mieszkania)
    apartment_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_apartments.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    media_type = Column(String(50), nullable=False)  # electricity | water
    # licznik nadrzędny: zużycie = własny odczyt - suma zużyć pozostałych mieszkań
    is_master = Column(Boolean, default=False, nullable=False)
    name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    apartment = relationship("RentalApartment", back_populates="meters")
    readings = relationship("RentalMeterReading", back_populates="meter", passive_deletes=True)


# ---------------------------------------------------------------------------
# Rozliczenia miesięczne
# ---------------------------------------------------------------------------


class RentalBillingPeriod(Base):
    __tablename__ = "rentals_billing_periods"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    period_month = Column(Date, unique=True, nullable=False)  # zawsze 1. dzień miesiąca
    status = Column(String(50), default="draft", nullable=False)  # draft | closed
    electricity_bill_amount = Column(Numeric(10, 2), nullable=True)
    electricity_rate = Column(Numeric(10, 4), nullable=True)  # zł/kWh — wyliczona lub nadpisana
    electricity_rate_is_manual = Column(Boolean, default=False, nullable=False)
    water_rate = Column(Numeric(10, 2), default=9.00, nullable=False)  # zł/m3
    note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    readings = relationship("RentalMeterReading", back_populates="period", passive_deletes=True)
    settlements = relationship("RentalSettlement", back_populates="period", passive_deletes=True)
    beneficiary_settlements = relationship("RentalBeneficiarySettlement", back_populates="period", passive_deletes=True)


class RentalMeterReading(Base):
    __tablename__ = "rentals_meter_readings"
    __table_args__ = (UniqueConstraint("period_id", "meter_id", name="uq_rentals_meter_readings_period_meter"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    period_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_billing_periods.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    meter_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_meters.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    previous_value = Column(Numeric(12, 3), nullable=False)  # "Ostatnio"
    current_value = Column(Numeric(12, 3), nullable=False)  # "Teraz"
    # "Błąd_Licznika" — korekta z podziału błędu licznika głównego, edytowalna
    error_correction = Column(Numeric(12, 3), default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    period = relationship("RentalBillingPeriod", back_populates="readings")
    meter = relationship("RentalMeter", back_populates="readings")


class RentalSettlement(Base):
    __tablename__ = "rentals_settlements"
    __table_args__ = (UniqueConstraint("period_id", "apartment_id", name="uq_rentals_settlements_period_apartment"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    period_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_billing_periods.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    apartment_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_apartments.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    # NULL = pustostan (mieszkanie bez najemcy w tym okresie)
    tenancy_id = Column(UUID(as_uuid=True), ForeignKey("rentals_tenancies.id", ondelete="RESTRICT"), nullable=True)
    rent_amount = Column(Numeric(10, 2), default=0, nullable=False)  # snapshot czynszu z najmu
    electricity_consumption = Column(Numeric(12, 3), default=0, nullable=False)  # kWh po korektach
    electricity_cost = Column(Numeric(10, 2), default=0, nullable=False)
    water_consumption = Column(Numeric(12, 3), default=0, nullable=False)  # m3
    water_cost = Column(Numeric(10, 2), default=0, nullable=False)
    # media + koszty stałe + korekty (odpowiednik "Razem" z notatek, bez czynszu)
    total_media_amount = Column(Numeric(10, 2), default=0, nullable=False)
    total_amount = Column(Numeric(10, 2), default=0, nullable=False)  # total_media_amount + rent_amount
    note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    period = relationship("RentalBillingPeriod", back_populates="settlements")
    apartment = relationship("RentalApartment", back_populates="settlements")
    tenancy = relationship("RentalTenancy", back_populates="settlements")
    items = relationship(
        "RentalSettlementItem",
        back_populates="settlement",
        passive_deletes=True,
        order_by="RentalSettlementItem.created_at",
    )
    beneficiary_settlement_items = relationship(
        "RentalBeneficiarySettlementItem", back_populates="settlement", passive_deletes=True
    )


class RentalSettlementItem(Base):
    __tablename__ = "rentals_settlement_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    settlement_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_settlements.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    cost_type_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_cost_types.id", ondelete="RESTRICT"), nullable=True
    )  # NULL = korekta
    name = Column(String(255), nullable=False)  # snapshot nazwy ("śmieci", "zaległe media", "nadpłata")
    kind = Column(String(50), nullable=False)  # fixed_cost | adjustment
    amount = Column(Numeric(10, 2), nullable=False)  # może być ujemna
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    settlement = relationship("RentalSettlement", back_populates="items")
    cost_type = relationship("RentalCostType", back_populates="settlement_items")


# ---------------------------------------------------------------------------
# Podział rodzinny
# ---------------------------------------------------------------------------


class RentalBeneficiary(Base):
    __tablename__ = "rentals_beneficiaries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)  # "Ja", "Ojciec", "Mama"
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    allocation_rules = relationship("RentalAllocationRule", back_populates="beneficiary", passive_deletes=True)
    settlements = relationship("RentalBeneficiarySettlement", back_populates="beneficiary", passive_deletes=True)


class RentalAllocationRule(Base):
    __tablename__ = "rentals_allocation_rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    beneficiary_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_beneficiaries.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    # NULL = dotyczy wszystkich mieszkań / nie dotyczy mieszkania (recurring)
    apartment_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_apartments.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    component = Column(String(50), nullable=False)  # rent | electricity | water | cost_type | recurring
    cost_type_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_cost_types.id", ondelete="RESTRICT"), nullable=True
    )  # dla cost_type
    mode = Column(String(50), nullable=False)  # fixed_amount | full
    amount = Column(Numeric(10, 2), nullable=True)  # wymagane dla fixed_amount/recurring; może być ujemna
    description = Column(String(255), nullable=True)  # etykieta pozycji (np. "podatek", "telefon")
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    beneficiary = relationship("RentalBeneficiary", back_populates="allocation_rules")
    apartment = relationship("RentalApartment", back_populates="allocation_rules")
    cost_type = relationship("RentalCostType", back_populates="allocation_rules")
    beneficiary_settlement_items = relationship(
        "RentalBeneficiarySettlementItem", back_populates="rule", passive_deletes=True
    )


class RentalBeneficiarySettlement(Base):
    __tablename__ = "rentals_beneficiary_settlements"
    __table_args__ = (
        UniqueConstraint("period_id", "beneficiary_id", name="uq_rentals_beneficiary_settlements_period_beneficiary"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    period_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_billing_periods.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    beneficiary_id = Column(
        UUID(as_uuid=True), ForeignKey("rentals_beneficiaries.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    total_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    period = relationship("RentalBillingPeriod", back_populates="beneficiary_settlements")
    beneficiary = relationship("RentalBeneficiary", back_populates="settlements")
    items = relationship(
        "RentalBeneficiarySettlementItem",
        back_populates="beneficiary_settlement",
        passive_deletes=True,
        order_by="RentalBeneficiarySettlementItem.created_at",
    )


class RentalBeneficiarySettlementItem(Base):
    __tablename__ = "rentals_beneficiary_settlement_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    beneficiary_settlement_id = Column(
        UUID(as_uuid=True),
        ForeignKey("rentals_beneficiary_settlements.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    description = Column(String(255), nullable=False)  # np. "czynsz Dudzik", "woda — Pokój Łukasza"
    amount = Column(Numeric(10, 2), nullable=False)
    rule_id = Column(UUID(as_uuid=True), ForeignKey("rentals_allocation_rules.id", ondelete="RESTRICT"), nullable=True)
    settlement_id = Column(UUID(as_uuid=True), ForeignKey("rentals_settlements.id", ondelete="RESTRICT"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    beneficiary_settlement = relationship("RentalBeneficiarySettlement", back_populates="items")
    rule = relationship("RentalAllocationRule", back_populates="beneficiary_settlement_items")
    settlement = relationship("RentalSettlement", back_populates="beneficiary_settlement_items")
