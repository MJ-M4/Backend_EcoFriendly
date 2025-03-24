# backend/Interface/users.py
from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Optional
from http import HTTPStatus

from Models.user import User
from DataLayer.errors import (
    INVALID_INPUT_DATA,
    DB_USER_NOT_FOUND,
    DB_CONNECTION_ERROR,
    DB_QUERY_ERROR,
    DB_USER_ALREADY_EXISTS
)

class UserRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    role: Literal['manager','worker'] = 'worker'
    name: str = Field(..., min_length=1)
    phone: Optional[str] = None
    location: Optional[str] = None
    joining_date: Optional[str] = None
    worker_type: Optional[str] = None

class UserResponse(BaseModel):
    user_id: str
    role: Literal['manager','worker']
    name: str
    phone: Optional[str]
    location: Optional[str]
    joining_date: Optional[str]
    worker_type: Optional[str]

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])
def get_all_users():
    try:
        user_obj = User()
        data = user_obj.get_all_users()
        resp = [UserResponse(**u).dict() for u in data]
        return jsonify(resp), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error."}), HTTPStatus.INTERNAL_SERVER_ERROR

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user_obj = User()
        user_obj.load_by_id(user_id)
        resp = UserResponse(
            user_id=user_obj.user_id,
            role=user_obj.role,
            name=user_obj.name,
            phone=user_obj.phone,
            location=user_obj.location,
            joining_date=user_obj.joining_date,
            worker_type=user_obj.worker_type
        ).dict()
        return jsonify(resp), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg == DB_USER_NOT_FOUND:
            return jsonify({'message': "User not found."}), HTTPStatus.NOT_FOUND
        elif msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error."}), HTTPStatus.INTERNAL_SERVER_ERROR

@users_bp.route('', methods=['POST'])
def create_user():
    try:
        data = UserRequest(**request.get_json())
        user_obj = User().add_user(data.dict())
        resp = UserResponse(
            user_id=user_obj.user_id,
            role=user_obj.role,
            name=user_obj.name,
            phone=user_obj.phone,
            location=user_obj.location,
            joining_date=user_obj.joining_date,
            worker_type=user_obj.worker_type
        ).dict()
        return jsonify(resp), HTTPStatus.CREATED
    except ValidationError:
        return jsonify({'message': INVALID_INPUT_DATA}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        msg = str(e)
        if msg == DB_USER_ALREADY_EXISTS:
            return jsonify({'message': msg}), HTTPStatus.CONFLICT
        elif msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error."}), HTTPStatus.INTERNAL_SERVER_ERROR

@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_obj = User()
        user_obj.delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'}), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg == DB_USER_NOT_FOUND:
            return jsonify({'message': "User not found."}), HTTPStatus.NOT_FOUND
        elif msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error."}), HTTPStatus.INTERNAL_SERVER_ERROR
