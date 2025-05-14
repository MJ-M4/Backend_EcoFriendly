from http import HTTPStatus
from flask import Blueprint, jsonify, request
from src.interface.auth import auth_required
from src.errors import ErrorMessage
from src.errors.handlers import ApiError
from src.dal import bin_dal
from src.models.bin import Bin
from src.models.bin_reading import BinReading

bp = Blueprint("bins", __name__, url_prefix="/bins")


# ───────────── CRUD ─────────────
@bp.post("/")
@auth_required(role="manager")
def create_bin():
    data = request.get_json(silent=True) or {}
    bin_ = Bin.model_validate(data)
    bin_dal.create(bin_)
    return jsonify(bin_.model_dump()), HTTPStatus.CREATED.value


@bp.get("/")
@auth_required()
def list_bins():
    return jsonify([b.model_dump() for b in bin_dal.list_all()])


@bp.get("/<int:bin_id>")
@auth_required()
def get_bin(bin_id: int):
    return jsonify(bin_dal.get(bin_id).model_dump())


@bp.put("/<int:bin_id>")
@auth_required(role="manager")
def update_bin(bin_id: int):
    fields = request.get_json(silent=True) or {}
    bin_ = bin_dal.update(bin_id, **fields)
    return jsonify(bin_.model_dump())


@bp.delete("/<int:bin_id>")
@auth_required(role="manager")
def delete_bin(bin_id: int):
    bin_dal.delete(bin_id)
    return jsonify(status="deleted")


# ───────────── Readings ─────────────
@bp.get("/readings/<int:bin_id>")
@auth_required()
def get_readings(bin_id: int):
    # simple example: latest 50 readings
    from sqlalchemy import text
    from src.dal.database import get_session
    from src.dal._base import _row_to_model

    query = text(
        """
        SELECT reading_id, bin_id, level_pct, ts
        FROM BinReadings
        WHERE bin_id=:bid
        ORDER BY ts DESC
        LIMIT 50
        """
    )
    with get_session() as sess:
        rows = sess.execute(query, {"bid": bin_id}).all()
    return jsonify([_row_to_model(r, BinReading).model_dump() for r in rows])
