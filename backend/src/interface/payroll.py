from http import HTTPStatus
from flask import Blueprint, jsonify, request, g

from src.interface.auth import auth_required
from src.errors import ErrorMessage
from src.errors.handlers import ApiError
from src.dal import payroll_dal
from src.models.payroll import Payroll

bp = Blueprint("payroll", __name__, url_prefix="/payroll")


# ───────────── CRUD (manager) ─────────────
@bp.post("/")
@auth_required(role="manager")
def create_payroll():
    p = Payroll.model_validate(request.get_json(silent=True) or {})
    payroll_dal.create(p)
    return jsonify(p.model_dump()), HTTPStatus.CREATED.value


@bp.get("/")
@auth_required(role="manager")
def list_payroll():
    return jsonify([p.model_dump() for p in payroll_dal.list_all()])


@bp.get("/<int:payroll_id>")
@auth_required()
def get_payroll(payroll_id: int):
    p = payroll_dal.get(payroll_id)
    # employees may read only their own rows
    if g.current_role != "manager" and p.employee_id != g.current_user_id:
        raise ApiError(ErrorMessage.PERMISSION_DENIED, HTTPStatus.FORBIDDEN)
    return jsonify(p.model_dump())


@bp.put("/<int:payroll_id>")
@auth_required(role="manager")
def update_payroll(payroll_id: int):
    p = payroll_dal.update(payroll_id, **(request.get_json(silent=True) or {}))
    return jsonify(p.model_dump())


@bp.delete("/<int:payroll_id>")
@auth_required(role="manager")
def delete_payroll(payroll_id: int):
    payroll_dal.delete(payroll_id)
    return jsonify(status="deleted")


# ───────────── Mark paid ─────────────
@bp.post("/<int:payroll_id>/mark-paid")
@auth_required(role="manager")
def mark_paid(payroll_id: int):
    p = payroll_dal.update(payroll_id, paid=True)
    return jsonify(p.model_dump())