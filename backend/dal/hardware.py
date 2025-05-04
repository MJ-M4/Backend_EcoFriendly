from typing import Any
from Database.connection import DatabaseConnection
from common.errors import ErrorMessage as EM

class HardwareDAL:
    def __init__(self):
        self._db = DatabaseConnection().conn()

    def _run(self, sql: str, params: tuple[Any, ...] = ()):
        cur = self._db.cursor()
        cur.execute(sql, params)
        self._db.commit()
        return cur

    # ---------- CRUD ----------
    def list(self):
        c = self._db.cursor(dictionary=True)
        c.execute("SELECT * FROM hardware")
        return c.fetchall()

    def get(self, hid: str):
        c = self._db.cursor(dictionary=True)
        c.execute("SELECT * FROM hardware WHERE id=%s", (hid,))
        row = c.fetchone()
        if not row:
            raise RuntimeError(EM.HARDWARE_NOT_FOUND)
        return row

    def create(self, data: dict):
        cols = ", ".join(data)
        ph   = ", ".join("%s" for _ in data)
        self._run(f"INSERT INTO hardware ({cols}) VALUES ({ph})", tuple(data.values()))

    def update(self, hid: str, data: dict):
        if not data:
            return
        sets  = ", ".join(f"{k}=%s" for k in data)
        parms = tuple(data.values()) + (hid,)
        cur   = self._run(f"UPDATE hardware SET {sets} WHERE id=%s", parms)
        if cur.rowcount == 0:
            raise RuntimeError(EM.HARDWARE_NOT_FOUND)

    def delete(self, hid: str):
        cur = self._run("DELETE FROM hardware WHERE id=%s", (hid,))
        if cur.rowcount == 0:
            raise RuntimeError(EM.HARDWARE_NOT_FOUND)

    # ---------- alerts ----------
    def alerts(self):
        c = self._db.cursor(dictionary=True)
        c.execute("SELECT * FROM hardware WHERE status='Needs Maintenance' OR battery<25")
        return c.fetchall()