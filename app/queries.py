from db import Database
from random import randint
from sqlalchemy.sql import text
from crypt import hash_password

class Queries:
    def __init__(self, db):
        self.db = db

    def generate_unique_id(self):
        while True:
            new_id = randint(10000001, 99999999)
            sql = "SELECT id FROM user_credentials WHERE id = :id"
            result = self.db.conn.session.execute(text(sql), {'id': new_id}).fetchone()
            if not result:
                return new_id

    def get_user_by_username(self, username):
        sql = "SELECT id, username, password, tier FROM user_credentials WHERE username = :username"
        result = self.db.conn.session.execute(text(sql), {'username': username}).fetchone()
        if result:
            return {
                'id': result.id,
                'username': result.username,
                'password': result.password,
                'tier': result.tier
            }
        return None

    def create_user(self, firstname, surname, email, username, password, tier, postal_code):
        hashed_password = hash_password(password)
        new_id = self.generate_unique_id()
        credds_sql = "INSERT INTO user_credentials (id, username, password, tier) VALUES (:id, :username, :password, :tier)"
        details_sql = "INSERT INTO user_details (user_id, firstname, surname, email, postal_code) VALUES (:user_id, :firstname, :surname, :email, :postal_code)"
        self.db.conn.session.execute(text(credds_sql), {'id': new_id, 'username': username, 'password': hashed_password, 'tier': tier})
        self.db.conn.session.execute(text(details_sql), {'user_id': new_id, 'firstname': firstname, 'surname': surname, 'email': email, 'postal_code': postal_code})
        self.db.conn.session.commit()

    def get_user_by_username_or_email(self, username, email):
        sql = "SELECT uc.username, ud.email FROM user_credentials uc JOIN user_details ud ON uc.id = ud.user_id WHERE uc.username = :username OR ud.email = :email"
        result = self.db.conn.session.execute(text(sql), {'username': username, 'email': email}).fetchone()
        if result:
            return {
                'username': result.username,
                'email': result.email
            }
        return None
    
    def get_user_details(self, user_id):
        sql = "SELECT firstname, surname, email, postal_code FROM user_details WHERE user_id = :user_id"
        result = self.db.conn.session.execute(text(sql), {'user_id': user_id}).fetchone()
        if result:
            return {
                'firstname': result.firstname,
                'surname': result.surname,
                'email': result.email,
                'postal_code': result.postal_code
            }
        return None

    def update_user_tier(self, username, new_tier):
        sql = "UPDATE user_credentials SET tier = :tier WHERE username = :username"
        self.db.conn.session.execute(text(sql), {'tier': new_tier, 'username': username})
        self.db.conn.session.commit()

    def search_users(self, query):
        sql = "SELECT username FROM user_credentials WHERE username ILIKE :query"
        result = self.db.conn.session.execute(text(sql), {'query': f"{query}%"}).fetchall()
        return [{'username': row.username} for row in result]
    
    def add_observation(self, user_id, postal_area_id, temperature, cloudiness, precipitation_amount, precipitation_type, observation_time):
        sql_check = """
        SELECT id FROM observations
        WHERE user_id = :user_id
        AND postal_area_id = :postal_area_id
        AND date_trunc('hour', observation_time) = date_trunc('hour', :observation_time)
        """
        result = self.db.conn.session.execute(text(sql_check), {
            'user_id': user_id,
            'postal_area_id': postal_area_id,
            'observation_time': observation_time
        }).fetchone()

        if result:
            sql_update = """
            UPDATE observations
            SET temperature = :temperature,
                cloudiness = :cloudiness,
                precipitation_amount = :precipitation_amount,
                precipitation_type = :precipitation_type,
                observation_time = :observation_time
            WHERE id = :id
            """
            self.db.conn.session.execute(text(sql_update), {
                'temperature': temperature,
                'cloudiness': cloudiness,
                'precipitation_amount': precipitation_amount,
                'precipitation_type': precipitation_type,
                'observation_time': observation_time,
                'id': result.id
            })
        else:
            sql_insert = """
            INSERT INTO observations (user_id, postal_area_id, temperature, cloudiness, precipitation_amount, precipitation_type, observation_time)
            VALUES (:user_id, :postal_area_id, :temperature, :cloudiness, :precipitation_amount, :precipitation_type, :observation_time)
            """
            self.db.conn.session.execute(text(sql_insert), {
                'user_id': user_id,
                'postal_area_id': postal_area_id,
                'temperature': temperature,
                'cloudiness': cloudiness,
                'precipitation_amount': precipitation_amount,
                'precipitation_type': precipitation_type,
                'observation_time': observation_time
            })
        self.db.conn.session.commit()

    def get_parameters(self):
        sql = "SELECT id, description FROM parameters"
        result = self.db.conn.session.execute(text(sql)).fetchall()
        return [{'id': row.id, 'description': row.description} for row in result]
    
    def get_postal_areas(self):
        sql = "SELECT id, postal_code, name FROM postal_areas"
        result = self.db.conn.session.execute(text(sql)).fetchall()
        return [{'id': row.id, 'postal_code': row.postal_code, 'name': row.name} for row in result]
    

    
    def get_postal_area_id_by_code(self, postal_code):
        sql = "SELECT id FROM postal_areas WHERE postal_code = :postal_code"
        result = self.db.conn.session.execute(text(sql), {'postal_code': postal_code}).fetchone()
        return result.id if result else None
    
    def get_observations(self, tier, start_time, end_time, postal_code=None):
        sql = """
        SELECT o.*, pa.postal_code, uc.username FROM observations o
        JOIN postal_areas pa ON o.postal_area_id = pa.id
        JOIN user_credentials uc ON o.user_id = uc.id
        WHERE o.observation_time BETWEEN :start_time AND :end_time
        """
        if postal_code:
            sql += " AND pa.postal_code = :postal_code"
        sql += " LIMIT 100"
        result = self.db.conn.session.execute(text(sql), {
            'start_time': start_time,
            'end_time': end_time,
            'postal_code': postal_code
        }).fetchall()

        observations = [dict(row._mapping) for row in result]
        if tier != 'admin':
            for observation in observations:
                observation.pop('id', None)
        return observations
    
    def get_forecasts(self, tier, start_time, end_time, postal_code=None):
        sql = """
        SELECT f.*, pa.postal_code, uc.username FROM forecasts f
        JOIN postal_areas pa ON f.postal_area_id = pa.id
        JOIN user_credentials uc ON f.user_id = uc.id
        WHERE f.forecast_time BETWEEN :start_time AND :end_time
        """
        if postal_code:
            sql += " AND pa.postal_code = :postal_code"
        sql += " LIMIT 100"
        result = self.db.conn.session.execute(text(sql), {
            'start_time': start_time,
            'end_time': end_time,
            'postal_code': postal_code
        }).fetchall()
        
        forecasts = [dict(row._mapping) for row in result]
        if tier != 'admin':
            for forecast in forecasts:
                forecast.pop('id', None)
        return forecasts
    
    def search_observations(self, query):
        sql = "SELECT id FROM observations WHERE id::text ILIKE :query"
        result = self.db.conn.session.execute(text(sql), {'query': f"{query}%"}).fetchall()
        return [{'id': row.id} for row in result]
    
    def delete_observation(self, observation_id):
        sql = "DELETE FROM observations WHERE id = :id"
        self.db.conn.session.execute(text(sql), {'id': observation_id})
        self.db.conn.session.commit()

    def add_forecast(self, user_id, postal_area_id, forecast_data):
        for forecast in forecast_data:
            existing_forecast = self.get_forecast(user_id, postal_area_id, forecast['forecast_time'], forecast['analysis_time'])
            if existing_forecast:
                self.update_forecast(user_id, postal_area_id, forecast)
            else:
                sql_insert = """
                INSERT INTO forecasts (user_id, postal_area_id, temperature, cloudiness, precipitation_amount, precipitation_type, forecast_time, analysis_time)
                VALUES (:user_id, :postal_area_id, :temperature, :cloudiness, :precipitation_amount, :precipitation_type, :forecast_time, :analysis_time)
                """
                self.db.conn.session.execute(text(sql_insert), {
                    'user_id': user_id,
                    'postal_area_id': postal_area_id,
                    'temperature': forecast['temperature'],
                    'cloudiness': forecast['cloudiness'],
                    'precipitation_amount': forecast['precipitation_amount'],
                    'precipitation_type': forecast['precipitation_type'],
                    'forecast_time': forecast['forecast_time'],
                    'analysis_time': forecast['analysis_time']
                })
        self.db.conn.session.commit()

    def get_forecast(self, user_id, postal_area_id, forecast_time, analysis_time):
        sql = """
        SELECT id FROM forecasts
        WHERE user_id = :user_id AND postal_area_id = :postal_area_id
        AND forecast_time = :forecast_time AND analysis_time = :analysis_time
        """
        result = self.db.conn.session.execute(text(sql), {
            'user_id': user_id,
            'postal_area_id': postal_area_id,
            'forecast_time': forecast_time,
            'analysis_time': analysis_time
        }).fetchone()
        return result

    def update_forecast(self, user_id, postal_area_id, forecast):
        sql_update = """
        UPDATE forecasts
        SET temperature = :temperature, cloudiness = :cloudiness,
            precipitation_amount = :precipitation_amount, precipitation_type = :precipitation_type
        WHERE user_id = :user_id AND postal_area_id = :postal_area_id
        AND forecast_time = :forecast_time AND analysis_time = :analysis_time
        """
        self.db.conn.session.execute(text(sql_update), {
            'user_id': user_id,
            'postal_area_id': postal_area_id,
            'temperature': forecast['temperature'],
            'cloudiness': forecast['cloudiness'],
            'precipitation_amount': forecast['precipitation_amount'],
            'precipitation_type': forecast['precipitation_type'],
            'forecast_time': forecast['forecast_time'],
            'analysis_time': forecast['analysis_time']
        })
        self.db.conn.session.commit()
