# backend/Interface/auth.py
from flask import Blueprint, request, jsonify
from Models.user import User
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from http import HTTPStatus
from DataLayer.errors import INVALID_INPUT_DATA, DB_USER_NOT_FOUND, DB_INVALID_CREDENTIALS

# Pydantic models for request and response validation
class LoginRequest(BaseModel):
    user_id: str = Field(..., min_length=1, description="User ID (e.g., 207705096)")
    password: str = Field(..., min_length=1, description="User password")

class LoginResponse(BaseModel):
    user_id: str
    role: Literal['manager', 'worker']
    name: str
    phone: str | None
    location: str | None
    joining_date: str | None
    worker_type: Literal['Driver', 'Cleaner', 'Maintenance Worker'] | None

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # Validate request data using Pydantic
        data = LoginRequest(**request.get_json())
        
        # Perform login
        user = User()
        user = user.login(data.user_id, data.password)
        
        # Prepare response using Pydantic
        response_data = LoginResponse(**user.to_dict())
        return jsonify(response_data.dict()), HTTPStatus.OK

    except ValidationError as e:
        return jsonify({'message': INVALID_INPUT_DATA}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        error_message = str(e)
        if error_message in [DB_USER_NOT_FOUND, DB_INVALID_CREDENTIALS]:
            return jsonify({'message': error_message}), HTTPStatus.UNAUTHORIZED
        return jsonify({'message': error_message}), HTTPStatus.INTERNAL_SERVER_ERROR