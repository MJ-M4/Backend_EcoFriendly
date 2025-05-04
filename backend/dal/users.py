from typing import Any
import bcrypt
from Database.connection import DatabaseConnection
from common.errors import ErrorMessage as EM

class UsersDAL:
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
        c.execute("SELECT user_id,name,role,phone,location,joining_date,worker_type FROM users")
        return c.fetchall()

    def get(self, uid: str):
        c = self._db.cursor(dictionary=True)
        c.execute("SELECT * FROM users WHERE user_id=%s", (uid,))
        row = c.fetchone()
        if not row:
            raise RuntimeError(EM.USER_NOT_FOUND)
        return row

    def create(self, data: dict):
        cur = self._db.cursor()
        cur.execute("SELECT 1 FROM users WHERE user_id=%s", (data["user_id"],))
        if cur.fetchone():
            raise RuntimeError(EM.USER_EXISTS)
        hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
        data = {**data, "password": hashed}
        cols = ", ".join(data)
        ph   = ", ".join("%s" for _ in data)
        self._run(f"INSERT INTO users ({cols}) VALUES ({ph})", tuple(data.values()))

    def update(self, uid: str, data: dict):
        if not data:
            return
        sets  = ", ".join(f"{k}=%s" for k in data)
        parms = tuple(data.values()) + (uid,)
        cur   = self._run(f"UPDATE users SET {sets} WHERE user_id=%s", parms)
        if cur.rowcount == 0:
            raise RuntimeError(EM.USER_NOT_FOUND)

    def delete(self, uid: str):
        cur = self._run("DELETE FROM users WHERE user_id=%s", (uid,))
        if cur.rowcount == 0:
            raise RuntimeError(EM.USER_NOT_FOUND)

    # ---------- auth helpers ----------
    def verify(self, uid: str, raw_password: str):
        row = self.get(uid)  # may raise USER_NOT_FOUND
        if not bcrypt.checkpw(raw_password.encode(), row["password"].encode()):
            raise RuntimeError(EM.INVALID_CREDENTIALS)
        # remove password before returning
        row.pop("password", None)
        return row
