# backend/routes/vehicles.py
from flask import Blueprint, request, jsonify
from extensions import db  # Import db from extensions.py
from models.vehicle import Vehicle  # You'll need to create this model

vehicles_bp = Blueprint('vehicles', __name__)

@vehicles_bp.route('/', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{
        'id': vehicle.id,
        'type': vehicle.type,
        'license_plate': vehicle.license_plate,
        'status': vehicle.status,
        'last_maintenance': vehicle.last_maintenance.isoformat() if vehicle.last_maintenance else None
    } for vehicle in vehicles]), 200

@vehicles_bp.route('/', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    vehicle = Vehicle(
        type=data['type'],
        license_plate=data['license_plate'],
        status=data.get('status', 'Available'),
        last_maintenance=data.get('last_maintenance')
    )
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle added successfully', 'id': vehicle.id}), 201

@vehicles_bp.route('/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle deleted successfully'}), 200