from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.datalayer.bin_data import fetch_all_bins, add_bin, delete_bin_by_id
from src.models.bin_model import BinCreate
from src.errors.general_errors import DataFetchError

bin_bp = Blueprint("bins", __name__)

@bin_bp.route("/getBins", methods=["GET"])
def get_bins():
    try:
        bins = fetch_all_bins()
        # print(f"The data received for fetching bins is: {bins}")
        return jsonify({"status": "success", "bins": bins}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@bin_bp.route("/addBin", methods=["POST"])
def create_bin():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), HTTPStatus.BAD_REQUEST
        
        bin_data = BinCreate.model_validate(data)
        result = add_bin(bin_data)
        return jsonify({"status": "success", "message": "Bin added successfully", "bin": result}), HTTPStatus.CREATED
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), HTTPStatus.CONFLICT
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.BAD_REQUEST
    

@bin_bp.route("/deleteBin/<binId>", methods=["DELETE"])
def delete_bin(binId):
    try:
        delete_bin_by_id(binId)
        return jsonify({"status": "success", "message": "Bin deleted"}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR