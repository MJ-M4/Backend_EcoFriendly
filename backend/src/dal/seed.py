"""
Seed script – populate Roles, first manager, and 3 demo bins.
Run:  `python -m src.dal.seed`
"""
import bcrypt
from sqlalchemy import text

from src.dal.database import ENGINE


def run_seed():
    with ENGINE.begin() as conn:
        # ─────────────── Roles ───────────────
        conn.execute(
            text(
                "INSERT IGNORE INTO Roles(role_id, role_name) "
                "VALUES (1,'manager'), (2,'employee')"
            )
        )

        # ─────────────── First Manager ───────
        pwd_hash = bcrypt.hashpw(b"1234", bcrypt.gensalt()).decode()
        conn.execute(
            text(
                """
                INSERT IGNORE INTO Users(
                    user_id, role_id, first_name, last_name, password_hash, is_active
                )
                VALUES (:uid, 1, 'First', 'Manager', :pwd, TRUE)
                """
            ),
            {"uid": 207705096, "pwd": pwd_hash},
        )

        # ─────────────── Sample Bins ────────
        bins = [
            ("HQ-Front-Door", 240),
            ("Warehouse-Dock-1", 660),
            ("Main-Street-Corner", 1100),
        ]
        conn.execute(
            text(
                "INSERT IGNORE INTO Bins(location, capacity_l) VALUES "
                ", ".join("(:loc{i}, :cap{i})".format(i=i) for i in range(len(bins)))
            ),
            {f"loc{i}": b[0] for i, b in enumerate(bins)}
            | {f"cap{i}": b[1] for i, b in enumerate(bins)}
        )
    print("✔️  Database seeded")


if __name__ == "__main__":
    run_seed()
