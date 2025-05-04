from typing import Any
from Database.connection import DatabaseConnection
from common.errors import ErrorMessage as EM

class PaymentsDAL:
    def __init__(self):
        self._db = DatabaseConnection().conn()

    def _run(self, sql: str, params: tuple[Any, ...] = ()):
        cur = self._db.cursor()
        cur.execute(sql, params)
        self._db.commit()
        return cur

    def list(self):
        c = self._db.cursor(dictionary=True)
        c.execute("SELECT * FROM payments")
        return c.fetchall()

    def get(self, pid: int):
        c = self._db.cursor(dictionary=True)
        c.execute("SELECT * FROM payments WHERE id=%s", (pid,))
        row = c.fetchone()
        if not row:
            raise RuntimeError(EM.PAYMENT_NOT_FOUND)
        return row

    def create(self, data: dict):
        cols = ", ".join(data)
        ph   = ", ".join("%s" for _ in data)
        self._run(f"INSERT INTO payments ({cols}) VALUES ({ph})", tuple(data.values()))

    def set_paid(self, pid: int, paid_date: str):
        cur = self._run(
            "UPDATE payments SET status='Paid', payment_date=%s WHERE id=%s",
            (paid_date, pid),
        )
        if cur.rowcount == 0:
            raise RuntimeError(EM.PAYMENT_NOT_FOUND)

    def delete(self, pid: int):
        cur = self._run("DELETE FROM payments WHERE id=%s", (pid,))
        if cur.rowcount == 0:
            raise RuntimeError(EM.PAYMENT_NOT_FOUND)
