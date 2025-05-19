from flask import Blueprint, request, jsonify, make_response
from Models.Employee import Employee
from pydantic import BaseModel, ValidationError
from http import HTTPStatus

employees_bp = Blueprint('employees', __name__)

class EmployeeModel(BaseModel):
    identity: str
    name: str
    phone: str
    location: str
    joining_date: str
    worker_type: str
    password: str 

@employees_bp.route('/getEmployees', methods=['GET'])
def get_employees():
    employees = Employee.get_all()
    return make_response(jsonify([e.to_dict() for e in employees]), HTTPStatus.OK)

@employees_bp.route('/addEmployees', methods=['POST'])
def add_employee():
    try:
        data = EmployeeModel(**request.get_json())
    except ValidationError as e:
        return make_response(jsonify({'error': e.errors()}), HTTPStatus.BAD_REQUEST)
    
    employee = Employee.create(
        identity=data.identity,
        name=data.name,
        phone=data.phone,
        location=data.location,
        joining_date=data.joining_date,
        worker_type=data.worker_type,
        password=data.password  
    )
    return make_response(jsonify(employee.to_dict()), HTTPStatus.CREATED)

# @employees_bp.route('/<int:employee_id>', methods=['PUT'])
# def update_employee(employee_id):
#     employee = Employee.get_by_id(employee_id)
#     if not employee:
#         return make_response(jsonify({'error': 'Employee not found'}), HTTPStatus.NOT_FOUND)
    
#     req_data = request.get_json()
#     employee.update(
#         identity=req_data.get('identity'),
#         name=req_data.get('name'),
#         phone=req_data.get('phone'),
#         location=req_data.get('location'),
#         joining_date=req_data.get('joining_date'),
#         worker_type=req_data.get('worker_type')
#     )
#     return make_response(jsonify(employee.to_dict()), HTTPStatus.OK)

@employees_bp.route('/deleteEmployees<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.get_by_id(employee_id)
    if not employee:
        return make_response(jsonify({'error': 'Employee not found'}), HTTPStatus.NOT_FOUND)
    
    employee.delete()
    return make_response(jsonify({'message': 'Employee deleted successfully'}), HTTPStatus.OK)