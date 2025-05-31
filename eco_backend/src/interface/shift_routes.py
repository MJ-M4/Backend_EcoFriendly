from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.datalayer.shift_data import fetch_all_shifts,add_shift,delete_shift_by_id, update_shift
from src.models.shift_model import ShiftCreate, ShiftUpdate
from src.errors.general_errors import DataFetchError

shift_bp = Blueprint("shifts", __name__)

@shift_bp.route("/getShifts", methods=["GET"])
def get_shifts():
    try:
        shifts = fetch_all_shifts()
        if not shifts:
            raise DataFetchError("No shifts found")
        # print(f"The data received for fetching shifts is: {shifts}")
        return jsonify({"status": "success", "shifts": shifts}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@shift_bp.route("/addShift", methods=["POST"])
def create_shift():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), HTTPStatus.BAD_REQUEST
        
        shift_data = ShiftCreate.model_validate(data)
        result = add_shift(shift_data)
        return jsonify({"status": "success", "message": "Shift added successfully", "shift": result}), HTTPStatus.CREATED
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), HTTPStatus.CONFLICT
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.BAD_REQUEST
    
@shift_bp.route("/deleteShift/<shift_id>", methods=["DELETE"])
def delete_shift(shift_id: str):
    try:
        delete_shift_by_id(shift_id)
        return jsonify({"status": "success", "message": "Shift deleted"}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@shift_bp.route("/updateShift/<shift_id>", methods=["PUT"])
def update_shift_endpoint(shift_id: str):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), HTTPStatus.BAD_REQUEST
        shift_data = ShiftUpdate.model_validate(data)
        result = update_shift(shift_id, shift_data)
        return jsonify({"status": "success", "message": "Shift updated successfully", "shift": result}), HTTPStatus.OK
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), HTTPStatus.BAD_REQUEST
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
