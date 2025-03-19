import mysql.connector

config = {
    'host': 'localhost',
    'database': 'ecofriendly',
    'user': 'root',
    'password': '',
}

try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("Successfully connected to the database")
    connection.close()
except Exception as e:
    print(f"Error: {e}")