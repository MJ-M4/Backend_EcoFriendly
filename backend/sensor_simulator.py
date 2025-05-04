"""
Periodically “fills” bins and, when >80 %, inserts an empty‑task.
Run with:  python sensor_simulator.py      (or supervise it with pm2/systemd)
"""
import random, time, datetime
from http import HTTPStatus
from threading import Event

from Backend_EcoFriendly.backend.dal import bins
from Database.connection import DatabaseConnection
from common.errors import BIN_NOT_FOUND
# … inside tick()
from dal.bins import BinsDL
_dl = BinsDL()
# …
for b in bins:
    new_cap = min(100, b["capacity"] + random.randint(0, MAX_GROWTH))
    _dl._set_capacity(b["bin_id"], new_cap)
    # alert logic continues …


INTERVAL_MINUTES = 15                    # every quarter‑hour
MAX_GROWTH       = 12                    # % added per tick
ALERT_THRESHOLD  = 80

stop = Event()

def tick():
    db  = DatabaseConnection().get_connection()
    cur = db.cursor(dictionary=True)

    # 1. pick every bin
    cur.execute("SELECT bin_id, capacity FROM bins")
    bins = cur.fetchall()

    for b in bins:
        new_cap = min(100, b["capacity"] + random.randint(0, MAX_GROWTH))
        cur.execute("UPDATE bins SET capacity=%s WHERE bin_id=%s", (new_cap, b["bin_id"]))

        # 2. fire alert + task if exceeded threshold
        if new_cap >= ALERT_THRESHOLD:
            cur.execute(
                "INSERT IGNORE INTO tasks (bin_id, created_at, status) VALUES (%s,%s,'pending')",
                (b["bin_id"], datetime.datetime.utcnow())
            )
    db.commit()

def main():
    print("🔄  sensor simulator started – CTRL‑C to stop")
    while not stop.wait(INTERVAL_MINUTES * 60):
        try:
            tick()
            print(f"✔️  simulator ran at {datetime.datetime.utcnow().isoformat(timespec='seconds')}Z")
        except Exception as exc:
            print("❌  simulator error:", exc, flush=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop.set()
