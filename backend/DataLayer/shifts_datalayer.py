# backend/DataLayer/shifts_datalayer.py
import mysql.connector
from DataLayer.errors import DB_QUERY_ERROR
from Database.connection import DatabaseConnection

class ShiftsDataLayer:
    def __init__(self):
        self.db = DatabaseConnection()

    def insert_shift(self, shift_data):
        """
        shift_data = {
          worker_id, worker_name, worker_type, date,
          start_time, end_time, location, status
        }
        """
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO shifts (
                  worker_id, worker_name, worker_type,
                  date, start_time, end_time,
                  location, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                shift_data['worker_id'],
                shift_data['worker_name'],
                shift_data['worker_type'],
                shift_data['date'],
                shift_data['start_time'],
                shift_data['end_time'],
                shift_data['location'],
                shift_data['status'],
            )
            cursor.execute(query, values)
            conn.commit()
            shift_id = cursor.lastrowid
            cursor.close()
            return shift_id
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def fetch_shifts_by_worker(self, worker_id, status=None):
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            if status:
                query = "SELECT * FROM shifts WHERE worker_id = %s AND status = %s"
                cursor.execute(query, (worker_id, status))
            else:
                query = "SELECT * FROM shifts WHERE worker_id = %s"
                cursor.execute(query, (worker_id,))
            shifts = cursor.fetchall()
            cursor.close()
            for s in shifts:
                s['date'] = str(s['date'])
                s['start_time'] = str(s['start_time'])
                s['end_time'] = str(s['end_time'])
                if s.get('submitted_at'):
                    s['submitted_at'] = str(s['submitted_at'])
            return shifts
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def fetch_all_shifts(self, status=None):
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            if status:
                query = "SELECT * FROM shifts WHERE status = %s"
                cursor.execute(query, (status,))
            else:
                query = "SELECT * FROM shifts"
                cursor.execute(query)
            shifts = cursor.fetchall()
            cursor.close()
            for s in shifts:
                s['date'] = str(s['date'])
                s['start_time'] = str(s['start_time'])
                s['end_time'] = str(s['end_time'])
                if s.get('submitted_at'):
                    s['submitted_at'] = str(s['submitted_at'])
            return shifts
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def update_shift_status(self, shift_id, status):
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = "UPDATE shifts SET status = %s WHERE id = %s"
            cursor.execute(query, (status, shift_id))
            conn.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if rowcount == 0:
                raise Exception("Shift not found")
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def delete_shift(self, shift_id):
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = "DELETE FROM shifts WHERE id = %s"
            cursor.execute(query, (shift_id,))
            conn.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if rowcount == 0:
                raise Exception("Shift not found")
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()
