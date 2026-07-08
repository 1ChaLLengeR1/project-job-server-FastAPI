DROP TABLE IF EXISTS logs CASCADE;
DROP TABLE IF EXISTS outstandingmoney CASCADE;
DROP TABLE IF EXISTS namesoverdue CASCADE;
DROP TABLE IF EXISTS keyscalculatorpatryk CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS calendar_work_days CASCADE;
DROP TABLE IF EXISTS calendar_work_condition_changes CASCADE;

-- czysci stan migracji, zeby migration_up mogl odtworzyc schemat od zera
DROP TABLE IF EXISTS alembic_version;

DROP EXTENSION IF EXISTS "uuid-ossp";
