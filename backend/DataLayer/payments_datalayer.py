# backend/DataLayer/payments_datalayer.py
import mysql.connector
from Database.connection import DatabaseConnection
from DataLayer.errors import DB_QUERY_ERROR

class PaymentsDataLayer:
    def __init__(self):
        self.db = DatabaseConnection()

    def fetch_all_payments(self):
        """
        Returns a list of dictionaries, each representing one payment record.
        """
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM payments"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            # Convert date fields to string if needed
            for row in results:
                row['payment_date'] = str(row['payment_date'])
            return results
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def insert_payment(self, payment_data):
        """
        Inserts a new payment record.
        payment_data keys: worker_id, worker_name, amount, payment_date, status, notes
        """
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO payments (
                  worker_id, worker_name, amount, payment_date, status, notes
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                payment_data['worker_id'],
                payment_data['worker_name'],
                payment_data['amount'],
                payment_data['payment_date'],
                payment_data['status'],
                payment_data['notes'],
            )
            cursor.execute(query, values)
            conn.commit()
            new_id = cursor.lastrowid
            cursor.close()
            return new_id
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def update_payment_status(self, payment_id, new_status, new_date=None):
        """
        Updates the status of a payment record.
        If new_date is provided, update the payment_date as well.
        """
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor()

            if new_date:
                query = "UPDATE payments SET status = %s, payment_date = %s WHERE id = %s"
                cursor.execute(query, (new_status, new_date, payment_id))
            else:
                query = "UPDATE payments SET status = %s WHERE id = %s"
                cursor.execute(query, (new_status, payment_id))

            conn.commit()
            rowcount = cursor.rowcount
            cursor.close()

            if rowcount == 0:
                raise Exception("Payment not found")
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()

    def delete_payment(self, payment_id):
        """
        Delete a payment record by ID.
        """
        try:
            self.db.connect()
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = "DELETE FROM payments WHERE id = %s"
            cursor.execute(query, (payment_id,))
            conn.commit()
            rowcount = cursor.rowcount
            cursor.close()
            if rowcount == 0:
                raise Exception("Payment not found")
        except mysql.connector.Error as e:
            raise Exception(DB_QUERY_ERROR) from e
        finally:
            self.db.disconnect()
