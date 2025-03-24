# backend/Database/connection.py
import mysql.connector
from mysql.connector import Error
from DataLayer.errors import DB_CONNECTION_ERROR

class DatabaseConnection:
    """Singleton-like approach to connect/disconnect from MySQL."""

    def __init__(self, config=None):
        # Default config or override
        if config is None:
            config = {
                'host': 'localhost',
                'database': 'ecofriendly',
                'user': 'root',
                'password': '123456',
            }
        self.config = config
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("MySQL connection successful.")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise Exception(DB_CONNECTION_ERROR) from e

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed.")

    def get_connection(self):
        """Return the active connection (make sure to call connect() first)."""
        return self.connection
