import mysql.connector
from src.config_loader import load_config

class Database:
    def __init__(self):
        config = load_config()["mysql"]
        self.connection = mysql.connector.connect(
            host=config["host"],
            port=config.getint("port"),
            user=config["user"],
            password=config["password"],
            database=config["database"]
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def query(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def query_one(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
