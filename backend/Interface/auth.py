from flask import Blueprint, request, jsonify, make_response
from Models.User import User
from pydantic import BaseModel, ValidationError
from http import HTTPStatus

auth_bp = Blueprint('auth', __name__)

class LoginModel(BaseModel):
    username: str
    password: str
    role: str

class RegisterModel(BaseModel):
    username: str
    password: str
    role: str
    worker_type: str = "Other"

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = LoginModel(**request.get_json())
    except ValidationError as e:
        return make_response(jsonify({'error': e.errors()}), HTTPStatus.BAD_REQUEST)
    
    user = User.get_by_username(data.username)
    if user and user.check_password(data.password) and user.role == data.role:
        return make_response(jsonify({'message': 'Login successful', 'role': user.role}), HTTPStatus.OK)
    return make_response(jsonify({'error': 'Invalid credentials'}), HTTPStatus.UNAUTHORIZED)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = RegisterModel(**request.get_json())
    except ValidationError as e:
        return make_response(jsonify({'error': e.errors()}), HTTPStatus.BAD_REQUEST)
    
    if User.get_by_username(data.username):
        return make_response(jsonify({'error': 'User already exists'}), HTTPStatus.CONFLICT)
    
    user = User.create(
        username=data.username,
        role=data.role,
        password=data.password,
        worker_type=data.worker_type
    )
    return make_response(jsonify(user.to_dict()), HTTPStatus.CREATED)