# backend/DataLayer/bins_datalayer.py
from Database.connection import DatabaseConnection
from common.errors import BIN_NOT_FOUND
from datetime import datetime

class BinsDL:
    def __init__(self):
        self.db = DatabaseConnection().get_connection()

    # ---------- READ ----------
    def all(self):
        cur = self.db.cursor(dictionary=True)
        cur.execute("SELECT * FROM bins")
        return cur.fetchall()

    def by_id(self, bid: str):
        cur = self.db.cursor(dictionary=True)
        cur.execute("SELECT * FROM bins WHERE bin_id=%s", (bid,))
        row = cur.fetchone()
        if not row:
            raise RuntimeError(BIN_NOT_FOUND)
        return row

    # ---------- CREATE ----------
    def add(self, data: dict):
        sql = (
            "INSERT INTO bins "
            "(bin_id, location, address, status, capacity, route, battery, lat, lon, updated_at) "
            "VALUES (%(bin_id)s, %(location)s, %(address)s, %(status)s, %(capacity)s, "
            "%(route)s, %(battery)s, %(lat)s, %(lon)s, %(updated_at)s)"
        )
        data.setdefault("updated_at", datetime.utcnow())   # default now()
        cur = self.db.cursor()
        cur.execute(sql, data)
        self.db.commit()

    # ---------- DELETE ----------
    def delete(self, bid: str):
        cur = self.db.cursor()
        cur.execute("DELETE FROM bins WHERE bin_id=%s", (bid,))
        if cur.rowcount == 0:
            raise RuntimeError(BIN_NOT_FOUND)
        self.db.commit()

    # ---------- INTERNAL: used by simulator ----------
    def _set_capacity(self, bid: str, new_cap: int):
        cur = self.db.cursor()
        cur.execute(
            "UPDATE bins SET capacity=%s, status=%s, updated_at=UTC_TIMESTAMP() WHERE bin_id=%s",
            (
                new_cap,
                "Full" if new_cap >= 80 else ("Near Full" if new_cap >= 20 else "Empty"),
                bid,
            ),
        )
        self.db.commit()
