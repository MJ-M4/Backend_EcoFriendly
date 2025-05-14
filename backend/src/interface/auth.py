"""
Authentication blueprint
Path →   /api/auth/login        (handled automatically by register_blueprints)

Features
────────
• POST /login        – verify creds, return JWT + role name.
• auth_required()    – decorator for protecting other endpoints.
"""

from datetime import datetime, timedelta
from functools import wraps
from http import HTTPStatus
import os

from flask import Blueprint, current_app, g, jsonify, request
import jwt

from src.dal import user_dal
from src.errors import ErrorMessage
from src.errors.handlers import ApiError
from src.models.role import RoleName

bp = Blueprint("auth", __name__, url_prefix="/auth")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _jwt_secret() -> str:
    """Read secret from env (Serverless sets JWT_SECRET)."""
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET not configured in environment")
    return secret


def _encode_token(sub: int, role: str) -> str:
    payload = {
        "sub": sub,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=12),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, _jwt_secret(), algorithm="HS256")


def _decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, _jwt_secret(), algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise ApiError(ErrorMessage.INVALID_CREDENTIALS, HTTPStatus.UNAUTHORIZED) from exc
    except jwt.InvalidTokenError as exc:
        raise ApiError(ErrorMessage.INVALID_CREDENTIALS, HTTPStatus.UNAUTHORIZED) from exc


# ---------------------------------------------------------------------------
# Public decorator
# ---------------------------------------------------------------------------


def auth_required(role: str | list[str] | None = None):
    """
    Decorator to guard endpoints.

    Args:
        role:   None → any authenticated user.
                "manager" or "employee" or [... ] list   → restrict by role claim.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            hdr = request.headers.get("Authorization", "")
            if not hdr.startswith("Bearer "):
                raise ApiError(ErrorMessage.PERMISSION_DENIED, HTTPStatus.UNAUTHORIZED)

            token = hdr.removeprefix("Bearer ").strip()
            claims = _decode_token(token)

            g.current_user_id = claims["sub"]
            g.current_role = claims["role"]

            if role is not None and claims["role"] not in (
                role if isinstance(role, list) else [role]
            ):
                raise ApiError(ErrorMessage.PERMISSION_DENIED, HTTPStatus.FORBIDDEN)

            return func(*args, **kwargs)

        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# Route  – POST /api/auth/login
# ---------------------------------------------------------------------------


@bp.post("/login")
def login():
    """Body: { "id": 207705096, "password": "1234" } → { token, role }"""
    data = request.get_json(silent=True) or {}
    user_id = data.get("id")
    password = data.get("password", "")

    if not user_id or not password:
        raise ApiError(ErrorMessage.INVALID_CREDENTIALS, HTTPStatus.UNAUTHORIZED)

    user = user_dal.get_by_id(int(user_id))  # may raise USER_NOT_FOUND ApiError
    if not user.check_password(password):
        raise ApiError(ErrorMessage.INVALID_CREDENTIALS, HTTPStatus.UNAUTHORIZED)

    role_name = RoleName.MANAGER.value if user.is_manager() else RoleName.EMPLOYEE.value
    token = _encode_token(sub=user.user_id, role=role_name)

    return jsonify(token=token, role=role_name)
