from flask import Blueprint, jsonify
from src.datalayer.employee_data import get_all_employees
from src.errors.general_errors import DataFetchError
from src.statuses.employee_status import fetch_success

employee_bp = Blueprint('employee', __name__, url_prefix='/api/employees')

@employee_bp.route('/', methods=['GET'])
def list_employees():
    try:
        employees = get_all_employees()
        return jsonify(fetch_success(employees))
    except Exception as e:
        print(f"[EMPLOYEE FETCH ERROR] {e}")
        raise DataFetchError("Unable to retrieve employee data")
