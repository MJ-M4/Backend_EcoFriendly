from flask import Blueprint, request, jsonify
from src.models.user_model import LoginInput
from src.datalayer.employee_data import get_user_by_identity
from src.errors.auth_errors import InvalidCredentialsError
from src.statuses.auth_status import login_success
import hashlib

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            raise InvalidCredentialsError("No data provided")
        if 'identity' not in data or 'password' not in data:
            raise InvalidCredentialsError("Identity and password are required")
        # Log the data received for debugging purposes
        print(f"The data received for login is: {data}")
        identity = data.get('identity') 
        password = data.get('password')
        if not identity or not password:
            raise InvalidCredentialsError("Identity and password cannot be empty")
        login_input = LoginInput(identity=data['identity'], password=data['password'])

        user, stored_hash = get_user_by_identity(login_input.identity)

        if not user:
            raise InvalidCredentialsError("User not found")

        hash_input = hashlib.sha256(login_input.password.encode('utf-8')).hexdigest()
        if hash_input != stored_hash:
            raise InvalidCredentialsError("Incorrect password")

        return login_success(user)  # returns a full `jsonify(...)` object already

    except InvalidCredentialsError as e:
        return jsonify({"status": "error", "message": e.message})
    
    except Exception as e:
        print(f"[LOGIN ERROR] {e}")
        return jsonify({"status": "error", "message": "Internal server error"})
