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

