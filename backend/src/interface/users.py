"""
Users / Employees API
Base path:  /api/users

End-points
──────────
POST   /                – create employee  (manager only)
GET    /                – list users       (manager only; ?q=search&limit=&offset=)
GET    /<id>            – retrieve single user (self or manager)
PUT    /<id>            – update fields        (self or manager)
DELETE /<id>            – delete user     (manager only)

POST   /<id>/generate-password
       → manager-only endpoint that creates a strong random password,
         stores the new hash, and returns the plaintext once.
"""

import secrets
from http import HTTPStatus
from typing import Any, Dict

from flask import Blueprint, jsonify, request, g

from src.interface.auth import auth_required
from src.errors import ErrorMessage
from src.errors.handlers import ApiError
from src import models
from src.dal import user_dal

bp = Blueprint("users", __name__, url_prefix="/users")

# ─────────────────────────── Helpers ────────────────────────────


def _require_self_or_manager(target_id: int):
    """Raise PERMISSION_DENIED unless current user is manager or same ID."""
    if g.current_role != "manager" and g.current_user_id != target_id:
        raise ApiError(ErrorMessage.PERMISSION_DENIED, HTTPStatus.FORBIDDEN)


# ─────────────────────────── Routes ─────────────────────────────


@bp.post("/")
@auth_required(role="manager")
def create_user():
    """Create a new employee (manager-only)."""
    payload: Dict[str, Any] = request.get_json(silent=True) or {}

    try:
        new_user = models.User.model_validate(payload)
    except Exception as exc:  # pydantic validation error
        raise ApiError(ErrorMessage.INVALID_CREDENTIALS, HTTPStatus.BAD_REQUEST) from exc

    # Force role = employee (2)
    new_user.role_id = 2
    user_dal.create(new_user)
    return jsonify(new_user.model_dump()), HTTPStatus.CREATED.value


@bp.get("/")
@auth_required(role="manager")
def list_users():
    """List users with optional ?q=search&limit=&offset=."""
    query = request.args.get("q", "").lower()
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))

    users = user_dal.list_all(limit=limit, offset=offset)
    if query:
        users = [u for u in users if query in u.full_name().lower()]

    return jsonify([u.model_dump() for u in users])


@bp.get("/<int:user_id>")
@auth_required()
def get_user(user_id: int):
    _require_self_or_manager(user_id)
    user = user_dal.get_by_id(user_id)
    return jsonify(user.model_dump())


@bp.put("/<int:user_id>")
@auth_required()
def update_user(user_id: int):
    _require_self_or_manager(user_id)
    fields = request.get_json(silent=True) or {}
    # Prevent role escalations by non-managers
    if g.current_role != "manager":
        fields.pop("role_id", None)

    user = user_dal.update(user_id, **fields)
    return jsonify(user.model_dump())


@bp.delete("/<int:user_id>")
@auth_required(role="manager")
def delete_user(user_id: int):
    user_dal.delete(user_id)
    return jsonify(status="deleted")


# ───────────────────── password generator ──────────────────────
@bp.post("/<int:user_id>/generate-password")
@auth_required(role="manager")
def generate_password(user_id: int):
    """Generate a strong random password for the given employee."""
    new_pw_plain = secrets.token_urlsafe(10)
    # pass raw password; model will hash via validator
    user_dal.update(user_id, password_hash=new_pw_plain)

    return jsonify(user_id=user_id, password=new_pw_plain)