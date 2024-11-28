-- Set role to wos_app
SET ROLE wos_app;

-- Drop existing tables if they exist
-- DROP TABLE IF EXISTS user_credentials CASCADE;
-- DROP TABLE IF EXISTS user_details CASCADE;
DROP TABLE IF EXISTS parameters CASCADE;
DROP TABLE IF EXISTS regions CASCADE;
DROP TABLE IF EXISTS municipalities CASCADE;
DROP TABLE IF EXISTS postal_areas CASCADE;
DROP TABLE IF EXISTS observations CASCADE;

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

-- Create regions table
CREATE TABLE regions (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- Create municipalities table
CREATE TABLE municipalities (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code INTEGER UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    region_id INTEGER REFERENCES regions(id) ON DELETE CASCADE
);

-- Create postal_areas table
CREATE TABLE postal_areas (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    postal_code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    municipality_code INTEGER REFERENCES municipalities(code) ON DELETE CASCADE
);

-- Create observations table
CREATE TABLE observations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_credentials(id) ON DELETE CASCADE,
    postal_area_id INTEGER REFERENCES postal_areas(id) ON DELETE CASCADE,
    temperature REAL,
    cloudiness INTEGER,
    precipitation_amount INTEGER,
    precipitation_type INTEGER,
    observation_time TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Create indexes
CREATE INDEX idx_user_credentials_username ON user_credentials(username);
CREATE INDEX idx_user_details_email ON user_details(email);
CREATE INDEX idx_postal_areas_postal_code ON postal_areas(postal_code);
CREATE INDEX idx_observations_user_id ON observations(user_id);
CREATE INDEX idx_observations_postal_area_id ON observations(postal_area_id);
CREATE INDEX idx_observations_observation_time ON observations(observation_time);