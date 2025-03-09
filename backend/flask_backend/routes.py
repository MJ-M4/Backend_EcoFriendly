from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_backend.model import User, db
from flask_backend.register import Register

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    identity = data.get('identity')
    password = data.get('password')

    if not identity or not password:
        return jsonify({"error": "ID and password are required"}), 400

    user = User.query.filter_by(identity=identity).first()
    if user is None or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid ID or password"}), 401

    return jsonify({
        "message": "Login successful!",
        "id": user.identity,
        "role": user.role,
        "worker_type": user.worker_type
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json() or {}
    identity = data.get('identity')
    password = data.get('password')
    role = data.get('role', 'worker')
    worker_type = data.get('worker_type')
    phone = data.get('phone')
    location = data.get('location')
    name = data.get('name')  # Add name
    joining_date = data.get('joiningDate')  # Add joiningDate (note the camelCase from frontend)
    registration = Register(
        identity=identity,
        password=password,
        role=role,
        worker_type=worker_type,
        phone=phone,
        location=location,
        name=name,
        joining_date=joining_date
    )
    response, status_code = registration.register_user()
    return jsonify(response), status_code

@auth_bp.route('/update-password', methods=['PUT'])
def update_password():
    data = request.get_json()
    identity = data.get('identity')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not identity or not current_password or not new_password:
        return jsonify({"error": "All fields are required"}), 400

    user = User.query.filter_by(identity=identity).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user.password, current_password):
        return jsonify({"error": "Current password is incorrect"}), 401

    user.password = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password updated successfully!"}), 200


