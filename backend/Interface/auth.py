# backend/Interface/auth.py
from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from http import HTTPStatus

from Models.user import User
from DataLayer.errors import (
    INVALID_INPUT_DATA,
    DB_USER_NOT_FOUND,
    DB_INVALID_CREDENTIALS,
    DB_CONNECTION_ERROR,
    DB_QUERY_ERROR
)

class LoginRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class LoginResponse(BaseModel):
    user_id: str
    role: Literal['manager','worker']
    name: str
    phone: str | None = None
    location: str | None = None
    joining_date: str | None = None
    worker_type: str | None = None

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = LoginRequest(**request.get_json())
        user = User().login(data.user_id, data.password)
        resp_data = {
            'user_id': user.user_id,
            'role': user.role,
            'name': user.name,
            'phone': user.phone,
            'location': user.location,
            'joining_date': user.joining_date,
            'worker_type': user.worker_type
        }
        validated = LoginResponse(**resp_data)
        return jsonify(validated.dict()), HTTPStatus.OK
    except ValidationError:
        return jsonify({'message': INVALID_INPUT_DATA}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        msg = str(e)
        if msg in [DB_USER_NOT_FOUND, DB_INVALID_CREDENTIALS]:
            return jsonify({'message': msg}), HTTPStatus.UNAUTHORIZED
        elif msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error."}), HTTPStatus.INTERNAL_SERVER_ERROR
