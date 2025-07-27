CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SET client_encoding TO 'UTF8';

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255),
    password VARCHAR(255),
    type VARCHAR(255)
);

CREATE TABLE keyscalculatorpatryk (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    income_tax FLOAT,
    vat FLOAT,
    inpost_parcel_locker FLOAT,
    inpost_courier FLOAT,
    inpost_cash_of_delivery_courier FLOAT,
    dpd FLOAT,
    allegro_matt FLOAT,
    without_smart FLOAT
);

CREATE TABLE namesoverdue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255)
);

CREATE TABLE outstandingmoney (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    amount FLOAT,
    name VARCHAR(255),
    date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    id_name UUID
);

CREATE TABLE logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255),
    description TEXT,
    date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    description VARCHAR(255),
    time INTEGER,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE work_days (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE UNIQUE NOT NULL,
    hours_worked FLOAT,
    is_holiday BOOLEAN NOT NULL DEFAULT FALSE,
    norm_hours FLOAT NOT NULL,
    hourly_rate FLOAT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE work_condition_changes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    start_date DATE NOT NULL,
    norm_hours FLOAT NOT NULL,
    hourly_rate FLOAT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


