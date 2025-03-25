# backend/DataLayer/users_datalayer.py
import mysql.connector
from DataLayer.errors import DB_QUERY_ERROR, DB_USER_NOT_FOUND
from Database.connection import DatabaseConnection

class UsersDataLayer:
    def __init__(self):
        self.db = DatabaseConnection()

    def fetch_user_by_id(self, user_id):
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            cursor.close()
            if not user:
                raise Exception(DB_USER_NOT_FOUND)
            if user.get('joining_date'):
                user['joining_date'] = str(user['joining_date'])
            return user
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def fetch_all_users(self):
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM users"
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.close()
            for u in users:
                if u['joining_date']:
                    u['joining_date'] = str(u['joining_date'])
            return users
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def insert_user(self, user_data):
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO users (user_id, password, role, name, phone, location, joining_date, worker_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                user_data['user_id'],
                user_data['password'],
                user_data['role'],
                user_data['name'],
                user_data['phone'],
                user_data['location'],
                user_data['joining_date'],
                user_data['worker_type'],
            )
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def delete_user(self, user_id):
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = "DELETE FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            conn.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if rowcount == 0:
                raise Exception(DB_USER_NOT_FOUND)
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def update_user_password(self, user_id, new_hashed_password):
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = "UPDATE users SET password = %s WHERE user_id = %s"
            cursor.execute(query, (new_hashed_password, user_id))
            conn.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if rowcount == 0:
                raise Exception(DB_USER_NOT_FOUND)
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()
