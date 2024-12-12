import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

class Database:
    def __init__(self):
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_host = os.getenv('DB_HOST')
        self.db_port = os.getenv('DB_PORT')
        self.db_name = os.getenv('DB_NAME')
        self.conn = None

    def connect(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.conn = SQLAlchemy(app)

    def check_connection(self):
        try:
            self.conn.session.execute(text('SELECT 1'))
            return True, ""
        except Exception as e:
            print(f"Error checking database connection: {e}")
            return False, "Tietokantayhteyttä ei voitu muodostaa, tarkista yhteysasetukset ja -parametrit"

    def check_tables(self):
        try:
            required_tables = [
                'user_credentials', 'user_details', 'parameters', 'regions', 
                'municipalities', 'postal_areas', 'observations', 'forecasts'
            ]
            for table in required_tables:
                self.conn.session.execute(text(f'SELECT 1 FROM {table} LIMIT 1'))
            return True, ""
        except Exception as e:
            print(f"Error checking database tables: {e}")
            return False, "Tietokannan schema ei oikein, tarvittavia tauluja ei löytynyt"
