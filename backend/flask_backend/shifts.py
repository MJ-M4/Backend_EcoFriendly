from flask import Blueprint, request, jsonify
from flask_backend.model import db, User, Shift
import logging
from datetime import datetime

shifts_bp = Blueprint('shifts', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@shifts_bp.route('/', methods=['GET'])
def get_shifts():
    logger.debug("GET /shifts route hit")
    try:
        shifts = Shift.query.all()
        data = [
            {
                "id": shift.id,
                "workerId": str(shift.worker_id),  # Convert to string for JSON
                "workerName": User.query.filter_by(identity=shift.worker_id).first().name if User.query.filter_by(identity=shift.worker_id).first() else "Unknown",
                "workerType": User.query.filter_by(identity=shift.worker_id).first().worker_type if User.query.filter_by(identity=shift.worker_id).first() else "N/A",
                "phone": User.query.filter_by(identity=shift.worker_id).first().phone if User.query.filter_by(identity=shift.worker_id).first() else "N/A",
                "date": shift.date.isoformat() if shift.date else "",
                "startTime": shift.start_time.strftime('%H:%M') if shift.start_time else "",
                "endTime": shift.end_time.strftime('%H:%M') if shift.end_time else "",
                "location": shift.location or ""
            } for shift in shifts
        ]
        logger.debug(f"Returning shifts data: {data}")
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error in get_shifts: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@shifts_bp.route('/', methods=['POST'])
def add_shift():
    logger.debug("POST /shifts -> add_shift")
    data = request.get_json() or {}
    logger.debug(f"Request JSON: {data}")

    required = ["workerId", "date", "startTime", "endTime", "location"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    worker = User.query.filter_by(identity=int(data["workerId"])).first()
    if not worker:
        return jsonify({"error": "Worker ID not found"}), 404
    if data.get("workerType") and worker.worker_type != data.get("workerType"):
        return jsonify({"error": f"Worker type mismatch. Expected {worker.worker_type}, got {data.get('workerType')}"}), 400

    try:
        shift_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        start_time = datetime.strptime(data["startTime"], "%H:%M").time()
        end_time = datetime.strptime(data["endTime"], "%H:%M").time()

        new_shift = Shift(
            worker_id=int(data["workerId"]),
            date=shift_date,
            start_time=start_time,
            end_time=end_time,
            location=data["location"]
        )
        db.session.add(new_shift)
        db.session.commit()
        return jsonify({
            "message": "Shift added successfully",
            "id": new_shift.id,
            "workerId": str(new_shift.worker_id),
            "date": new_shift.date.isoformat(),
            "startTime": new_shift.start_time.strftime('%H:%M'),
            "endTime": new_shift.end_time.strftime('%H:%M'),
            "location": new_shift.location
        }), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": "Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding shift: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@shifts_bp.route('/<int:shift_id>', methods=['DELETE'])
def delete_shift(shift_id):
    logger.debug(f"DELETE /shifts/{shift_id} route hit")
    try:
        shift = Shift.query.get_or_404(shift_id)
        db.session.delete(shift)
        db.session.commit()
        logger.debug(f"Successfully deleted shift with id: {shift_id}")
        return jsonify({"message": "Shift deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting shift: {str(e)}")
        return jsonify({"error": "Failed to delete shift", "details": str(e)}), 500

@shifts_bp.route('/<int:shift_id>', methods=['PUT'])
def update_shift(shift_id):
    logger.debug(f"PUT /shifts/{shift_id} route hit")
    data = request.get_json() or {}
    logger.debug(f"Request JSON: {data}")

    required = ["workerId", "date", "startTime", "endTime", "location"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    shift = Shift.query.get_or_404(shift_id)
    worker = User.query.filter_by(identity=int(data["workerId"])).first()
    if not worker:
        return jsonify({"error": "Worker ID not found"}), 404

    try:
        shift.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        shift.start_time = datetime.strptime(data["startTime"], "%H:%M").time()
        shift.end_time = datetime.strptime(data["endTime"], "%H:%M").time()
        shift.location = data["location"]
        db.session.commit()
        return jsonify({"message": "Shift updated successfully"}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": "Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating shift: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500