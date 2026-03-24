-- Runs automatically on first boot via docker-entrypoint-initdb.d
-- Creates the users table inside the "usersdb" database

CREATE TABLE IF NOT EXISTS users (
    id       SERIAL       PRIMARY KEY,
    name     VARCHAR(100) NOT NULL,
    email    VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP  DEFAULT NOW()
);