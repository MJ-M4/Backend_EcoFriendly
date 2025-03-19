# backend/Interface/users.py
from flask import Blueprint, request, jsonify
from Models.user import User
from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Optional
from http import HTTPStatus
from DataLayer.errors import INVALID_INPUT_DATA, DB_USER_NOT_FOUND, DB_INVALID_CREDENTIALS

class UserRequest(BaseModel):
    user_id: str = Field(..., min_length=1, description="User ID (e.g., 207705096)")
    password: str = Field(..., min_length=1, description="User password")
    role: Literal['manager', 'worker']
    name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    joining_date: str
    worker_type: Optional[Literal['Driver', 'Cleaner', 'Maintenance Worker']]

class UserResponse(BaseModel):
    user_id: str
    role: Literal['manager', 'worker']
    name: str
    phone: str
    location: str
    joining_date: str
    worker_type: Optional[Literal['Driver', 'Cleaner', 'Maintenance Worker']]
    password: Optional[str]

class PasswordUpdateRequest(BaseModel):
    current_password: str = Field(..., min_length=1, description="Current password")
    new_password: str = Field(..., min_length=1, description="New password")

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])
def get_all_users():
    try:
        print("Starting get_all_users endpoint")
        user = User()
        print("User object created")
        users = user.get_all_users()
        print(f"Fetched users: {users}")
        response_data = [UserResponse(**u).dict() for u in users]
        print(f"Response data: {response_data}")
        return jsonify(response_data), HTTPStatus.OK
    except Exception as e:
        print(f"Error in get_all_users: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@users_bp.route('', methods=['POST'])
def add_user():
    try:
        data = UserRequest(**request.get_json())
        user = User()
        user = user.add_user(data.dict())
        response_data = UserResponse(**user.to_dict())
        return jsonify(response_data.dict()), HTTPStatus.CREATED
    except ValidationError as e:
        return jsonify({'message': INVALID_INPUT_DATA}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({'message': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@users_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User()
        user.delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'}), HTTPStatus.OK
    except Exception as e:
        error_message = str(e)
        if error_message == DB_USER_NOT_FOUND:
            return jsonify({'message': error_message}), HTTPStatus.NOT_FOUND
        return jsonify({'message': error_message}), HTTPStatus.INTERNAL_SERVER_ERROR

@users_bp.route('/<user_id>/password', methods=['PUT'])
def update_password(user_id):
    try:
        data = PasswordUpdateRequest(**request.get_json())
        user = User()
        user.update_password(user_id, data.current_password, data.new_password)
        return jsonify({'message': 'Password updated successfully'}), HTTPStatus.OK
    except ValidationError as e:
        return jsonify({'message': INVALID_INPUT_DATA}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        error_message = str(e)
        if error_message == DB_USER_NOT_FOUND:
            return jsonify({'message': error_message}), HTTPStatus.NOT_FOUND
        if error_message == DB_INVALID_CREDENTIALS:
            return jsonify({'message': 'Current password is incorrect'}), HTTPStatus.UNAUTHORIZED
        return jsonify({'message': error_message}), HTTPStatus.INTERNAL_SERVER_ERROR