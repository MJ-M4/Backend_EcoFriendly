from flask import Blueprint, request, jsonify, make_response
from Models.Shift import Shift
from pydantic import BaseModel, ValidationError
from http import HTTPStatus

shifts_bp = Blueprint('shifts', __name__)

class ShiftModel(BaseModel):
    worker_id: int
    date: str
    start_time: str
    end_time: str
    location: str

@shifts_bp.route('/', methods=['GET'])
def get_shifts():
    shifts = Shift.get_all()
    return make_response(jsonify([shift.to_dict() for shift in shifts]), HTTPStatus.OK)

@shifts_bp.route('/', methods=['POST'])
def add_shift():
    try:
        data = ShiftModel(**request.get_json())
    except ValidationError as e:
        return make_response(jsonify({'error': e.errors()}), HTTPStatus.BAD_REQUEST)
    
    shift = Shift.create(
        worker_id=data.worker_id,
        date=data.date,
        start_time=data.start_time,
        end_time=data.end_time,
        location=data.location
    )
    return make_response(jsonify(shift.to_dict()), HTTPStatus.CREATED)

@shifts_bp.route('/<int:shift_id>', methods=['PUT'])
def update_shift(shift_id):
    shift = Shift.get_by_id(shift_id)
    if not shift:
        return make_response(jsonify({'error': 'Shift not found'}), HTTPStatus.NOT_FOUND)
    
    req_data = request.get_json()
    shift.update(
        worker_id=req_data.get('worker_id'),
        date=req_data.get('date'),
        start_time=req_data.get('start_time'),
        end_time=req_data.get('end_time'),
        location=req_data.get('location')
    )
    return make_response(jsonify(shift.to_dict()), HTTPStatus.OK)

@shifts_bp.route('/<int:shift_id>', methods=['DELETE'])
def delete_shift(shift_id):
    shift = Shift.get_by_id(shift_id)
    if not shift:
        return make_response(jsonify({'error': 'Shift not found'}), HTTPStatus.NOT_FOUND)
    
    shift.delete()
    return make_response(jsonify({'message': 'Shift deleted successfully'}), HTTPStatus.OK)