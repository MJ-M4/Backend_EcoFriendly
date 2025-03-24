# backend/DataLayer/vehicles_datalayer.py

import mysql.connector
from Database.connection import DatabaseConnection
from DataLayer.errors import DB_QUERY_ERROR

class VehiclesDataLayer:
    def __init__(self):
        self.db = DatabaseConnection()  # Our shared connection approach

    def fetch_all_vehicles(self):
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM vehicles")
            results = cursor.fetchall()
            cursor.close()

            # Convert DATE columns to string
            for row in results:
                if row['last_maintenance']:
                    row['last_maintenance'] = str(row['last_maintenance'])
            return results
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def insert_vehicle(self, vehicle_data):
        """
        vehicle_data = {
          'type': str,
          'license_plate': str,
          'status': str,
          'location': str,
          'last_maintenance': str (YYYY-MM-DD)
        }
        """
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO vehicles (type, license_plate, status, location, last_maintenance)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (
                vehicle_data['type'],
                vehicle_data['license_plate'],
                vehicle_data['status'],
                vehicle_data['location'],
                vehicle_data['last_maintenance'],
            )
            cursor.execute(query, values)
            conn.commit()
            inserted_id = cursor.lastrowid
            cursor.close()
            return inserted_id
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def delete_vehicle(self, vehicle_id):
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = "DELETE FROM vehicles WHERE id = %s"
            cursor.execute(query, (vehicle_id,))
            conn.commit()
            rowcount = cursor.rowcount
            cursor.close()

            if rowcount == 0:
                raise Exception("Vehicle not found")
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()
