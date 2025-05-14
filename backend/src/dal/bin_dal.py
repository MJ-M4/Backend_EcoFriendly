from sqlalchemy import text

from src.dal.database import get_session
from src.dal._base import _row_to_model
from src.errors import ErrorMessage
from src.errors.handlers import ApiError
from src.models.bin import Bin

_SELECT = "SELECT bin_id, location, capacity_l, last_emptied FROM Bins"
_INSERT = (
    "INSERT INTO Bins(location, capacity_l, last_emptied) "
    "VALUES (:loc, :cap, :le)"
)

def create(bin_: Bin) -> Bin:
    with get_session() as sess:
        res = sess.execute(
            text(_INSERT),
            {"loc": bin_.location, "cap": bin_.capacity_l, "le": bin_.last_emptied},
        )
        bin_.bin_id = res.lastrowid
    return bin_


def get(bin_id: int) -> Bin:
    with get_session() as sess:
        row = sess.execute(text(f"{_SELECT} WHERE bin_id=:bid"), {"bid": bin_id}).first()
        if not row:
            raise ApiError(ErrorMessage.BIN_NOT_FOUND)
        return _row_to_model(row, Bin)  # type: ignore[arg-type]


def list_all() -> list[Bin]:
    with get_session() as sess:
        rows = sess.execute(text(_SELECT)).all()
        return [_row_to_model(r, Bin) for r in rows]  # type: ignore[arg-type]


def update(bin_id: int, **fields) -> Bin:
    if not fields:
        return get(bin_id)
    sets = ", ".join(f"{k}=:{k}" for k in fields)
    with get_session() as sess:
        if not sess.execute(
            text(f"UPDATE Bins SET {sets} WHERE bin_id=:bid"), {"bid": bin_id, **fields}
        ).rowcount:
            raise ApiError(ErrorMessage.BIN_NOT_FOUND)
    return get(bin_id)


def delete(bin_id: int) -> None:
    with get_session() as sess:
        deleted = sess.execute(text("DELETE FROM Bins WHERE bin_id=:bid"), {"bid": bin_id}).rowcount
        if not deleted:
            raise ApiError(ErrorMessage.BIN_NOT_FOUND)