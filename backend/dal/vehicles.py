from typing import Any
from Database.connection import DatabaseConnection
from common.errors import ErrorMessage as EM

class VehiclesDAL:
    def __init__(self):
        self._db = DatabaseConnection().conn()

    def _run(self, sql: str, params: tuple[Any, ...] = ()):
        cur = self._db.cursor()
        cur.execute(sql, params)
        self._db.commit()
        return cur

    def list(self):
        c = self._db.cursor(dictionary=True)
        c.execute("SELECT * FROM vehicles")
        return c.fetchall()

    def get(self, vid: int):
        c = self._db.cursor(dictionary=True)
        c.execute("SELECT * FROM vehicles WHERE id=%s", (vid,))
        row = c.fetchone()
        if not row:
            raise RuntimeError(EM.VEHICLE_NOT_FOUND)
        return row

    def create(self, data: dict):
        cols = ", ".join(data)
        ph   = ", ".join("%s" for _ in data)
        self._run(f"INSERT INTO vehicles ({cols}) VALUES ({ph})", tuple(data.values()))

    def update(self, vid: int, data: dict):
        if not data:
            return
        sets  = ", ".join(f"{k}=%s" for k in data)
        parms = tuple(data.values()) + (vid,)
        cur   = self._run(f"UPDATE vehicles SET {sets} WHERE id=%s", parms)
        if cur.rowcount == 0:
            raise RuntimeError(EM.VEHICLE_NOT_FOUND)

    def delete(self, vid: int):
        cur = self._run("DELETE FROM vehicles WHERE id=%s", (vid,))
        if cur.rowcount == 0:
            raise RuntimeError(EM.VEHICLE_NOT_FOUND)
