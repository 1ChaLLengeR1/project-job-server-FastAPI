DELETE FROM logs;
DELETE FROM outstandingmoney;
DELETE FROM namesoverdue;
DELETE FROM keyscalculatorpatryk;
DELETE FROM users;
DELETE FROM tasks;

DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS outstandingmoney;
DROP TABLE IF EXISTS namesoverdue;
DROP TABLE IF EXISTS keyscalculatorpatryk;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tasks;

DROP EXTENSION IF EXISTS "uuid-ossp";
