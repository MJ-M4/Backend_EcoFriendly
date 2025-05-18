from src.models.user_model import User
from src.Database import Database
from mysql.connector import Error
from datetime import datetime

def get_all_employees():
    db = Database()
    query = "SELECT id, identity, name, phone, location, joining_date, worker_type, created_at FROM employees"
    rows = db.query(query)
    db.close()
    return rows
def get_user_by_identity(identity: str):
    try:
        db = Database()
        query = "SELECT * FROM employees WHERE identity = %s"
        row = db.query_one(query, (identity,))

        if row:
            created_at = row["created_at"] if isinstance(row["created_at"], datetime) else datetime.strptime(str(row["created_at"]), '%Y-%m-%d %H:%M:%S')
            user = User(
                user_id=row["id"],
                identity=row["identity"],
                name=row["name"],
                phone=row["phone"],
                location=row["location"],
                joining_date=row["joining_date"],
                role=row["role"],
                worker_type=row["worker_type"],
                created_at=created_at
            )
            return user, row["hashed_password"]
        return None, None
    except Error as e:
        print(f"[DB ERROR] {e}")
        return None, None
    finally:
        db.close()