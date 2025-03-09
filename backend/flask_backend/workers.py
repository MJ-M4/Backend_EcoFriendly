# workers.py
from flask import Blueprint, request, jsonify
from flask_backend.model import db, User
import logging
from datetime import datetime

workers_bp = Blueprint('workers', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@workers_bp.route('/', methods=['GET'], strict_slashes=False)
def get_workers():
    logger.debug("GET /workers route hit")
    try:
        users = User.query.all()
        data = []
        for u in users:
            data.append({
                "id": u.id,
                "identity": u.identity,
                "name": u.name or "",
                "phone": u.phone or "",
                "location": u.location or "",
                "joiningDate": u.joining_date.isoformat() if u.joining_date else "",
                "role": u.role,
                "workerType": u.worker_type or ""
            })
        logger.debug(f"Returning workers data: {data}")
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error in get_workers: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@workers_bp.route('/', methods=['POST'])
def add_worker():
    logger.debug("POST /workers -> add_worker")
    data = request.get_json() or {}
    logger.debug(f"Request JSON: {data}")

    required = ["identity", "name", "phone", "location", "joining_date", "worker_type"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    if User.query.filter_by(identity=data["identity"]).first():
        return jsonify({"error": "Worker with this identity already exists"}), 409

    date_obj = None
    if data["joining_date"]:
        try:
            date_obj = datetime.strptime(data["joining_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format, use YYYY-MM-DD"}), 400

    new_user = User(
        identity=data["identity"],
        password="",  # or hashed if desired
        role="worker",
        worker_type=data["worker_type"],
        phone=data["phone"],
        location=data["location"],
        name=data["name"],
        joining_date=date_obj
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "identity": new_user.identity,
        "name": new_user.name or "",
        "phone": new_user.phone or "",
        "location": new_user.location or "",
        "joiningDate": new_user.joining_date.isoformat() if new_user.joining_date else "",
        "role": new_user.role,
        "workerType": new_user.worker_type
    }), 201

@workers_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_worker(user_id):
    logger.debug(f"DELETE /workers/{user_id} route hit")
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        logger.debug(f"Successfully deleted user with id: {user_id}")
        return jsonify({"message": "Worker deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting worker: {str(e)}")
        return jsonify({"error": "Failed to delete worker", "details": str(e)}), 500