-- Set role to wos_app
SET ROLE wos_app;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS user_credentials CASCADE;
DROP TABLE IF EXISTS user_details CASCADE;

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

-- Create indexes
CREATE INDEX idx_user_credentials_username ON user_credentials(username);
CREATE INDEX idx_user_details_email ON user_details(email);