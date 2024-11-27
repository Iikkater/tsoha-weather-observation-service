-- Set role to wos_app
SET ROLE wos_app;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS user_credentials CASCADE;
DROP TABLE IF EXISTS user_details CASCADE;
DROP TABLE IF EXISTS parameters CASCADE;

-- Create user_credentials table
CREATE TABLE user_credentials (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    tier VARCHAR(20) DEFAULT 'basic' NOT NULL
);

-- Create user_details table
CREATE TABLE user_details (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_credentials(id) ON DELETE CASCADE,
    firstname VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Create parameters table
CREATE TABLE parameters (
    id SERIAL PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    unit VARCHAR(20) NOT NULL,
    datatype VARCHAR(20) NOT NULL,
    description TEXT NOT NULL
);

INSERT INTO parameters (id, code, unit, datatype, description) VALUES
(1, 'T', 'degC', 'real', 'Ilman lämpötila, hetkellinen'),
(2, 'CL', 'INT', 'integer', 'Pilvien määrä (selkeää[0], melko selkeää[1], puolipilvistä[2], melko pilvistä[3], pilvistä[4])'),
(3, 'PRA', 'INT', 'integer', 'Sateen intensiteetti (pouta[0], vähäistä sadetta[1], sadetta[2], runsasta sadetta[3])'),
(4, 'PRST', 'INT', 'integer', 'Sateen olomuoto (pouta[0], tihkua[1], vettä[2], räntää[3], lumijyväset[4], lunta[5], rakeita[6])');

-- Create indexes
CREATE INDEX idx_user_credentials_username ON user_credentials(username);
CREATE INDEX idx_user_details_email ON user_details(email);