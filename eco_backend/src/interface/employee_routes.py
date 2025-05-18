# src/interface/employee_routes.py

from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.datalayer.employee_data import (
    fetch_all_employees,
    add_employee,
    delete_employee_by_identity
)
from src.models.user_model import EmployeeCreate
from src.errors.general_errors import DataFetchError
from src.statuses.employee_status import fetch_success

employee_bp = Blueprint("employees", __name__, url_prefix="/api/employees")

@employee_bp.route("", methods=["GET"])
def get_employees():
    try:
        employees = fetch_all_employees()
        return fetch_success(employees)
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@employee_bp.route("", methods=["POST"])
def create_employee():
    try:
        data = request.get_json()
        emp = EmployeeCreate.model_validate(data)
        added = add_employee(emp)
        return jsonify(added), HTTPStatus.CREATED
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.BAD_REQUEST

@employee_bp.route("/<identity>", methods=["DELETE"])
def delete_employee(identity: str):
    try:
        delete_employee_by_identity(identity)
        return jsonify({"status": "success", "message": "Employee deleted"}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
