from flask import Blueprint, request, jsonify
from flask_backend.model import db, Vehicle  # Fixed import
from datetime import datetime
import logging

vehicles_bp = Blueprint('vehicles', __name__)
logger = logging.getLogger(__name__)

@vehicles_bp.route('/', methods=['GET'])
def get_vehicles():
    logger.debug("GET /vehicles -> get_vehicles")
    vehicles = Vehicle.query.all()
    return jsonify([{
        "id": v.id,
        "type": v.type,
        "licensePlate": v.license_plate,
        "status": v.status,
        "location": v.location,
        "lastMaintenance": v.last_maintenance.isoformat()
    } for v in vehicles]), 200

@vehicles_bp.route('/', methods=['POST'])
def add_vehicle():
    logger.debug("POST /vehicles -> add_vehicle")
    data = request.get_json() or {}
    logger.debug(f"Request JSON: {data}")

    required = ["type", "licensePlate", "status", "location", "lastMaintenance"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        last_maintenance = datetime.strptime(data["lastMaintenance"], "%Y-%m-%d").date()
        new_vehicle = Vehicle(
            type=data["type"],
            license_plate=data["licensePlate"],
            status=data["status"],
            location=data["location"],
            last_maintenance=last_maintenance
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify({
            "message": "Vehicle added successfully",
            "id": new_vehicle.id,
            "type": new_vehicle.type,
            "licensePlate": new_vehicle.license_plate,
            "status": new_vehicle.status,
            "location": new_vehicle.location,
            "lastMaintenance": new_vehicle.last_maintenance.isoformat()
        }), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding vehicle: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@vehicles_bp.route('/<int:id>', methods=['PUT'])
def update_vehicle(id):
    logger.debug(f"PUT /vehicles/{id} -> update_vehicle")
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    data = request.get_json() or {}
    logger.debug(f"Request JSON: {data}")

    required = ["type", "licensePlate", "status", "location", "lastMaintenance"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        vehicle.type = data["type"]
        vehicle.license_plate = data["licensePlate"]
        vehicle.status = data["status"]
        vehicle.location = data["location"]
        vehicle.last_maintenance = datetime.strptime(data["lastMaintenance"], "%Y-%m-%d").date()
        db.session.commit()
        return jsonify({
            "message": "Vehicle updated successfully",
            "id": vehicle.id,
            "type": vehicle.type,
            "licensePlate": vehicle.license_plate,
            "status": vehicle.status,
            "location": vehicle.location,
            "lastMaintenance": vehicle.last_maintenance.isoformat()
        }), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating vehicle: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@vehicles_bp.route('/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    logger.debug(f"DELETE /vehicles/{id} -> delete_vehicle")
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    try:
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify({"message": "Vehicle deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting vehicle: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500