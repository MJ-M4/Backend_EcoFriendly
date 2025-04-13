from flask import Blueprint, request, jsonify, make_response
from Models.Vehicle import Vehicle
from pydantic import BaseModel, ValidationError
from http import HTTPStatus

vehicles_bp = Blueprint('vehicles', __name__)

class VehicleModel(BaseModel):
    type: str
    license_plate: str
    status: str = "Available"
    last_maintenance: str = None
    location: str = None 

@vehicles_bp.route('/getVehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.get_all()
    return make_response(jsonify([v.to_dict() for v in vehicles]), HTTPStatus.OK)

@vehicles_bp.route('/addVehicles', methods=['POST'])
def add_vehicle():
    try:
        data = VehicleModel(**request.get_json())
    except ValidationError as e:
        return make_response(jsonify({'error': e.errors()}), HTTPStatus.BAD_REQUEST)
    
    vehicle = Vehicle.create(
        type=data.type,
        license_plate=data.license_plate,
        status=data.status,
        last_maintenance=data.last_maintenance,
        location=data.location 
    )
    return make_response(jsonify(vehicle.to_dict()), HTTPStatus.CREATED)

# @vehicles_bp.route('/<int:vehicle_id>', methods=['PUT'])
# def update_vehicle(vehicle_id):
#     vehicle = Vehicle.get_by_id(vehicle_id)
#     if not vehicle:
#         return make_response(jsonify({'error': 'Vehicle not found'}), HTTPStatus.NOT_FOUND)
    
#     req_data = request.get_json()
#     vehicle.update(
#         type=req_data.get('type'),
#         license_plate=req_data.get('license_plate'),
#         status=req_data.get('status'),
#         last_maintenance=req_data.get('last_maintenance'),
#         location=req_data.get('location')  # Added location
#     )
#     return make_response(jsonify(vehicle.to_dict()), HTTPStatus.OK)

@vehicles_bp.route('/deleteVehicles<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.get_by_id(vehicle_id)
    if not vehicle:
        return make_response(jsonify({'error': 'Vehicle not found'}), HTTPStatus.NOT_FOUND)
    
    vehicle.delete()
    return make_response(jsonify({'message': 'Vehicle deleted successfully'}), HTTPStatus.OK)