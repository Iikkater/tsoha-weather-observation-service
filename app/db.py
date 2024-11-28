import os
from flask_sqlalchemy import SQLAlchemy

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
