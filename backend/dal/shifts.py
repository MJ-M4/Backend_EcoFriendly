from typing import Any
from Database.connection import DatabaseConnection
from common.errors import ErrorMessage as EM

class ShiftsDAL:
    def __init__(self):
        self._db = DatabaseConnection().conn()

    def _run(self, sql: str, params: tuple[Any, ...] = ()):
        cur = self._db.cursor()
        cur.execute(sql, params)
        self._db.commit()
        return cur

    # ---------- CRUD ----------
    def list(self, status: str | None = None):
        c = self._db.cursor(dictionary=True)
        if status:
            c.execute("SELECT * FROM shifts WHERE status=%s", (status,))
        else:
            c.execute("SELECT * FROM shifts")
        return c.fetchall()

    def get(self, sid: int):
        c = self._db.cursor(dictionary=True)
        c.execute("SELECT * FROM shifts WHERE id=%s", (sid,))
        row = c.fetchone()
        if not row:
            raise RuntimeError(EM.SHIFT_NOT_FOUND)
        return row

    def create(self, data: dict) -> int:
        cols = ", ".join(data)
        ph   = ", ".join("%s" for _ in data)
        cur  = self._run(f"INSERT INTO shifts ({cols}) VALUES ({ph})", tuple(data.values()))
        return cur.lastrowid

    def update(self, sid: int, data: dict):
        if not data:
            return
        sets  = ", ".join(f"{k}=%s" for k in data)
        parms = tuple(data.values()) + (sid,)
        cur   = self._run(f"UPDATE shifts SET {sets} WHERE id=%s", parms)
        if cur.rowcount == 0:
            raise RuntimeError(EM.SHIFT_NOT_FOUND)

    def delete(self, sid: int):
        cur = self._run("DELETE FROM shifts WHERE id=%s", (sid,))
        if cur.rowcount == 0:
            raise RuntimeError(EM.SHIFT_NOT_FOUND)
