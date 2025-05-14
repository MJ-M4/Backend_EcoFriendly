from http import HTTPStatus
from flask import Blueprint, jsonify, request
from src.interface.auth import auth_required
from src.dal import vehicle_dal
from src.models.vehicle import Vehicle

bp = Blueprint("vehicles", __name__, url_prefix="/vehicles")

@bp.post("/")
@auth_required(role="manager")
def create_vehicle():
    data = request.get_json(silent=True) or {}
    v = Vehicle.model_validate(data)
    vehicle_dal.create(v)
    return jsonify(v.model_dump()), HTTPStatus.CREATED.value

@bp.get("/")
@auth_required()
def list_vehicles():
    return jsonify([v.model_dump() for v in vehicle_dal.list_all()])

@bp.get("/<int:vehicle_id>")
@auth_required()
def get_vehicle(vehicle_id: int):
    return jsonify(vehicle_dal.get(vehicle_id).model_dump())

@bp.put("/<int:vehicle_id>")
@auth_required(role="manager")
def update_vehicle(vehicle_id: int):
    v = vehicle_dal.update(vehicle_id, **(request.get_json(silent=True) or {}))
    return jsonify(v.model_dump())

@bp.delete("/<int:vehicle_id>")
@auth_required(role="manager")
def delete_vehicle(vehicle_id: int):
    vehicle_dal.delete(vehicle_id)
    return jsonify(status="deleted")
