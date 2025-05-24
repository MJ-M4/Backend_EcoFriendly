import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jayusi2024",
    database="ecofriendly"
)
print("Connected!" if conn.is_connected() else "Failed to connect.")
conn.close()
