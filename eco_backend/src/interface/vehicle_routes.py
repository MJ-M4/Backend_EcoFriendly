from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.datalayer.vehicle_data import fetch_all_vehicles, add_vehicle, delete_vehicle_by_id
from src.models.vehicle_model import VehicleCreate
from src.errors.general_errors import DataFetchError

vehicle_bp = Blueprint("vehicles", __name__)

@vehicle_bp.route("/getVehicles", methods=["GET"])
def get_vehicles():
    try:
        vehicles = fetch_all_vehicles()
        if not vehicles:
            raise DataFetchError("No vehicles found")
        # print(f"The data received for fetching vehicles is: {vehicles}")
        return jsonify({"status": "success", "vehicles": vehicles}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR



@vehicle_bp.route("/addVehicle", methods=["POST"])
def create_vehicle():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), HTTPStatus.BAD_REQUEST
        # print(f"The data received for creating a vehicle is: {data}")
        vehicle = VehicleCreate.model_validate(data)
        result = add_vehicle(vehicle)
        return jsonify({"status": "success", "message": "Vehicle added successfully", "vehicle": result}), HTTPStatus.CREATED
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), HTTPStatus.CONFLICT
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.BAD_REQUEST

@vehicle_bp.route("/deleteVehicle/<licensePlate>", methods=["DELETE"])
def delete_vehicle(licensePlate):
    try:
        delete_vehicle_by_id(licensePlate)
        return jsonify({"status": "success", "message": "Vehicle deleted"}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
