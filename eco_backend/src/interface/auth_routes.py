from flask import Blueprint, request, jsonify
from src.models.user_model import LoginInput
from src.datalayer.employee_data import get_user_by_identity
from src.errors.auth_errors import InvalidCredentialsError
from src.statuses.auth_status import login_success
import hashlib


auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        login_input = LoginInput(**data)

        user, stored_hash = get_user_by_identity(login_input.identity)

        if not user:
            raise InvalidCredentialsError("User not found")

        hash_input = hashlib.sha256(login_input.password.encode('utf-8')).hexdigest()
        if hash_input != stored_hash:
            raise InvalidCredentialsError("Incorrect password")

        return jsonify(login_success(user))

    except InvalidCredentialsError as e:
        return jsonify({"status": "error", "message": str(e)}), 401
    except Exception as e:
        print(f"[LOGIN ERROR] {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

