DROP TABLE IF EXISTS logs CASCADE;
DROP TABLE IF EXISTS outstandingmoney CASCADE;
DROP TABLE IF EXISTS namesoverdue CASCADE;
DROP TABLE IF EXISTS keyscalculatorpatryk CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS calendar_work_days CASCADE;
DROP TABLE IF EXISTS calendar_work_condition_changes CASCADE;

-- rentals: kolejnosc od dzieci do rodzicow (klucze obce ON DELETE RESTRICT)
DROP TABLE IF EXISTS rentals_beneficiary_settlement_items CASCADE;
DROP TABLE IF EXISTS rentals_beneficiary_settlements CASCADE;
DROP TABLE IF EXISTS rentals_allocation_rules CASCADE;
DROP TABLE IF EXISTS rentals_beneficiaries CASCADE;
DROP TABLE IF EXISTS rentals_settlement_items CASCADE;
DROP TABLE IF EXISTS rentals_settlements CASCADE;
DROP TABLE IF EXISTS rentals_meter_readings CASCADE;
DROP TABLE IF EXISTS rentals_billing_periods CASCADE;
DROP TABLE IF EXISTS rentals_meters CASCADE;
DROP TABLE IF EXISTS rentals_apartment_costs CASCADE;
DROP TABLE IF EXISTS rentals_cost_types CASCADE;
DROP TABLE IF EXISTS rentals_tenancies CASCADE;
DROP TABLE IF EXISTS rentals_tenants CASCADE;
DROP TABLE IF EXISTS rentals_apartments CASCADE;

-- czysci stan migracji, zeby migration_up mogl odtworzyc schemat od zera
DROP TABLE IF EXISTS alembic_version;

DROP EXTENSION IF EXISTS "uuid-ossp";
