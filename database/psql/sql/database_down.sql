DELETE FROM logs;
DELETE FROM outstandingmoney;
DELETE FROM namesoverdue;
DELETE FROM keyscalculatorpatryk;
DELETE FROM users;
DELETE FROM tasks;
DELETE FROM calendar_work_days;
DELETE FROM calendar_work_condition_changes;

DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS outstandingmoney;
DROP TABLE IF EXISTS namesoverdue;
DROP TABLE IF EXISTS keyscalculatorpatryk;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS calendar_work_days;
DROP TABLE IF EXISTS calendar_work_condition_changes;

DROP EXTENSION IF EXISTS "uuid-ossp";
