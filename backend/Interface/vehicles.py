# backend/Interface/vehicles.py

from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
from http import HTTPStatus

from Models.vehicle import Vehicle
from DataLayer.errors import (
    INVALID_INPUT_DATA,
    DB_CONNECTION_ERROR,
    DB_QUERY_ERROR
)

vehicles_bp = Blueprint('vehicles', __name__)

class VehicleRequest(BaseModel):
    # must match your table's columns
    type: Literal[
        'Garbage Truck','Van','Maintenance Vehicle','Electric Vehicle',
        'Sweeper Vehicle','Recycling Truck','Utility Vehicle','Compactor Truck',
        'Skip Truck','Water Tanker','Mini Truck'
    ]
    license_plate: str = Field(..., min_length=1)
    status: Literal['Available','In Use','Under Maintenance'] = 'Available'
    location: str
    last_maintenance: str  # e.g. "2025-02-01"

class VehicleResponse(BaseModel):
    id: int
    type: str
    license_plate: str
    status: str
    location: str
    last_maintenance: str | None

@vehicles_bp.route('', methods=['GET'])
def get_vehicles():
    """
    GET /api/vehicles
    """
    try:
        v_model = Vehicle()
        all_vehicles = v_model.get_all_vehicles()
        response_data = [VehicleResponse(**v).dict() for v in all_vehicles]
        return jsonify(response_data), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error occurred."}), HTTPStatus.INTERNAL_SERVER_ERROR

@vehicles_bp.route('', methods=['POST'])
def add_vehicle():
    """
    POST /api/vehicles
    { "type":"Garbage Truck", "license_plate":"ABC-123", "status":"Available",
      "location":"Nazareth", "last_maintenance":"2025-02-01" }
    """
    try:
        data = VehicleRequest(**request.get_json())
        vehicle_obj = Vehicle().create_vehicle(data.dict())
        resp = VehicleResponse(**vehicle_obj.to_dict()).dict()
        return jsonify(resp), HTTPStatus.CREATED
    except ValidationError:
        return jsonify({'message': INVALID_INPUT_DATA}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        msg = str(e)
        if msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        # e.g. "Duplicate entry" if license_plate not unique
        return jsonify({'message': msg}), HTTPStatus.BAD_REQUEST

@vehicles_bp.route('/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    """
    DELETE /api/vehicles/5
    """
    try:
        v_model = Vehicle()
        v_model.delete_vehicle(vehicle_id)
        return jsonify({'message': 'Vehicle deleted successfully'}), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg == "Vehicle not found":
            return jsonify({'message': msg}), HTTPStatus.NOT_FOUND
        elif msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error occurred."}), HTTPStatus.INTERNAL_SERVER_ERROR
