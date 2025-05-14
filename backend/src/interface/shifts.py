from datetime import datetime
from http import HTTPStatus
from flask import Blueprint, jsonify, request, g
from src.interface.auth import auth_required
from src.dal import shift_dal
from src.models.shift import Shift

bp = Blueprint("shifts", __name__, url_prefix="/shifts")


# ───────────── Manager endpoints ─────────────
@bp.post("/")
@auth_required(role="manager")
def create_shift():
    data = request.get_json(silent=True) or {}
    s = Shift.model_validate(data)
    shift_dal.create(s)
    return jsonify(s.model_dump()), HTTPStatus.CREATED.value


@bp.get("/")
@auth_required(role="manager")
def list_shifts():
    return jsonify([s.model_dump() for s in shift_dal.list_all()])


# ───────────── Worker view ─────────────
@bp.get("/my")
@auth_required()
def my_shifts():
    emp_id = g.current_user_id
    return jsonify([s.model_dump() for s in shift_dal.by_employee(emp_id)])
