from sqlalchemy import text, select

from src.dal.database import get_session
from src.dal._base import _row_to_model
from src.errors import ErrorMessage
from src.errors.handlers import ApiError
from src.models.user import User

# ─────────────────────────── Helpers ────────────────────────────
_SELECT = (
    "SELECT user_id, role_id, first_name, last_name, password_hash, is_active, created_at "
    "FROM Users"
)
_INSERT = (
    "INSERT INTO Users(user_id, role_id, first_name, last_name, password_hash, is_active) "
    "VALUES (:uid, :role, :fn, :ln, :pwd, :active)"
)
_UPDATE_BASE = "UPDATE Users SET "

# ─────────────────────────── CRUD API ───────────────────────────
def create(user: User) -> User:
    with get_session() as sess:
        sess.execute(
            text(_INSERT),
            {
                "uid": user.user_id,
                "role": user.role_id,
                "fn": user.first_name,
                "ln": user.last_name,
                "pwd": user.password_hash,
                "active": user.is_active,
            },
        )
    return user


def get_by_id(user_id: int) -> User:
    with get_session() as sess:
        row = sess.execute(text(f"{_SELECT} WHERE user_id=:uid"), {"uid": user_id}).first()
        if not row:
            raise ApiError(ErrorMessage.USER_NOT_FOUND)
        return _row_to_model(row, User)  # type: ignore[arg-type]


def list_all(limit: int = 100, offset: int = 0) -> list[User]:
    with get_session() as sess:
        rows = sess.execute(
            text(f"{_SELECT} ORDER BY created_at DESC LIMIT :lim OFFSET :off"),
            {"lim": limit, "off": offset},
        ).all()
        return [_row_to_model(r, User) for r in rows]  # type: ignore[arg-type]


def update(user_id: int, **fields) -> User:
    if not fields:
        return get_by_id(user_id)

    sets = ", ".join(f"{k}=:{k}" for k in fields.keys())
    q = text(f"{_UPDATE_BASE}{sets} WHERE user_id=:uid")
    params = {"uid": user_id, **fields}

    with get_session() as sess:
        if not sess.execute(q, params).rowcount:
            raise ApiError(ErrorMessage.USER_NOT_FOUND)
    return get_by_id(user_id)


def delete(user_id: int) -> None:
    with get_session() as sess:
        deleted = sess.execute(text("DELETE FROM Users WHERE user_id=:uid"), {"uid": user_id}).rowcount
        if not deleted:
            raise ApiError(ErrorMessage.USER_NOT_FOUND)
