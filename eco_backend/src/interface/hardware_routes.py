from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.datalayer.hardware_data import fetch_all_hardware, add_hardware, update_hardware_status
from src.models.hardware_model import HardwareCreate
from src.errors.general_errors import DataFetchError
from src.datalayer.hardware_data import delete_hardware_by_id

hardware_bp = Blueprint("hardware", __name__)

@hardware_bp.route("/getHardware", methods=["GET"])
def get_all_hardware():
    try:
        data = fetch_all_hardware()
        return jsonify({"status": "success", "hardware": data}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@hardware_bp.route("/addHardware", methods=["POST"])
def add_new_hardware():
    try:
        data = request.get_json()
        hw_data = HardwareCreate.model_validate(data)
        result = add_hardware(hw_data)
        return jsonify({"status": "success", "hardware": result}), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.BAD_REQUEST
    
@hardware_bp.route("/deleteHardware/<hw_id>", methods=["DELETE"])
def delete_hardware(hw_id):

    try:
        delete_hardware_by_id(hw_id)
        return jsonify({"status": "success", "message": "Hardware deleted"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.BAD_REQUEST


@hardware_bp.route("/updateHardware/<hw_id>", methods=["PUT"])
def update_hardware(hw_id):
    try:
        data = request.get_json()
        # Pass whatever status, but auto-override inside the datalayer
        result = update_hardware_status(hw_id, data.get("status", ""), data["battery"])
        return jsonify({"status": "success", "hardware": result}), HTTPStatus.OK
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.BAD_REQUEST