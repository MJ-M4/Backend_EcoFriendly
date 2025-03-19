# backend/DataLayer/database.py
import mysql.connector
from mysql.connector import Error
from DataLayer.errors import DB_CONNECTION_ERROR, DB_QUERY_ERROR, DB_USER_NOT_FOUND

class Database:
    def __init__(self):
        self.connection = None
        self.config = {
            'host': 'localhost',
            'database': 'ecofriendly',
            'user': 'root',
            'password': '123456',
        }

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Database connection successful")
                return True
        except Error as e:
            print(f"Database connection failed: {str(e)}")
            raise Exception(DB_CONNECTION_ERROR) from e
        return False

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

    def fetch_user_by_id(self, user_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            cursor.close()
            if not user:
                raise Exception(DB_USER_NOT_FOUND)
            # Convert joining_date to string
            if user['joining_date']:
                user['joining_date'] = str(user['joining_date'])
            print(f"Fetched user by ID: {user}")
            return user
        except Error as e:
            print(f"Error in fetch_user_by_id: {str(e)}")
            raise Exception(DB_QUERY_ERROR) from e

    def fetch_all_users(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM users"
            cursor.execute(query)
            users = cursor.fetchall()
            # Convert joining_date to string for each user
            for user in users:
                if user['joining_date']:
                    user['joining_date'] = str(user['joining_date'])
            cursor.close()
            print(f"Fetched users from database: {users}")
            return users
        except Error as e:
            print(f"Error fetching users: {str(e)}")
            raise Exception(DB_QUERY_ERROR) from e

    def insert_user(self, user_data):
        try:
            cursor = self.connection.cursor()
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
            self.connection.commit()
            cursor.close()
        except Error as e:
            raise Exception(DB_QUERY_ERROR) from e

    def delete_user(self, user_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            self.connection.commit()
            cursor.close()
            if cursor.rowcount == 0:
                raise Exception(DB_USER_NOT_FOUND)
        except Error as e:
            raise Exception(DB_QUERY_ERROR) from e