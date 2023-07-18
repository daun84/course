from models.ModelUser import ModelUser
from werkzeug.security import generate_password_hash

import sqlite3

class ControllerDatabase:

    @staticmethod
    def __connection():
        return sqlite3.connect("users.db")

    @staticmethod
    def setup_database():
        with ControllerDatabase.__connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    id INTEGER PRIMARY KEY AUTOINCREMENT
                ); 
            """)
        
    
    @staticmethod
    def register_user(user: ModelUser):
        try:
            with ControllerDatabase.__connection() as conn:
                cursor = conn.cursor()
                user_data_dict = {
                    'username': user.username,
                    'password': generate_password_hash(user.password)
                }
                cursor.execute(""" 
                    INSERT INTO users(username, password)
                    VALUES (:username, :password)""",
                    user_data_dict
                )
        except Exception as e:
            print(e)


    @staticmethod
    def get_user(username: str) -> ModelUser:
        user: ModelUser = None
        try:
            with ControllerDatabase.__connection() as conn:
                cursor = conn.cursor()
                cursor.execute(""" 
                    SELECT * FROM users
                    WHERE username =  :username""",
                    {'username': username}
                )
                data = cursor.fetchone()
                if data is not None:
                    user = ModelUser(*data)
        except Exception as e:
            print(e)
        return user

            
    @staticmethod
    def show():
        with ControllerDatabase.__connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM users
            """)
            print(cursor.fetchall())

