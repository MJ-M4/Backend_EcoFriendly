from flask import Blueprint, request, jsonify
from flask_backend.model import db, User
from werkzeug.security import check_password_hash, generate_password_hash
import logging

user_bp = Blueprint('user', __name__)  # Renamed from auth_bp to user_bp
logger = logging.getLogger(__name__)

@user_bp.route('/update-password/<int:user_id>', methods=['PUT'])
def update_password(user_id):
    logger.debug(f"PUT /user/update-password/{user_id} -> update_password")
    data = request.get_json() or {}
    logger.debug(f"Request JSON: {data}")

    required = ["currentPassword", "newPassword"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Verify current password
    if not check_password_hash(user.password, data["currentPassword"]):
        return jsonify({"error": "Current password is incorrect"}), 401

    # Validate new password
    if data["newPassword"] == data["currentPassword"]:
        return jsonify({"error": "New password must be different from the current password"}), 400

    # Hash and update the new password
    try:
        user.password = generate_password_hash(data["newPassword"])
        db.session.commit()
        return jsonify({"message": "Password updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating password: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500