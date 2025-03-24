# backend/Interface/shifts.py
from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Optional
from http import HTTPStatus

from Models.shift import Shift
from DataLayer.errors import (
    INVALID_INPUT_DATA,
    DB_USER_NOT_FOUND,
    DB_CONNECTION_ERROR,
    DB_QUERY_ERROR
)

class ShiftRequest(BaseModel):
    worker_id: str = Field(..., min_length=1)
    date: str = Field(..., description="YYYY-MM-DD")
    start_time: str = Field(..., description="HH:MM")
    end_time: str = Field(..., description="HH:MM")
    location: str = Field(..., min_length=1)
    status: Literal['pending','approved'] = 'pending'

class ShiftResponse(BaseModel):
    id: int
    worker_id: str
    worker_name: Optional[str]
    worker_type: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    date: str
    start_time: str
    end_time: str
    status: Literal['pending','approved','denied']
    submitted_at: Optional[str] = None

shifts_bp = Blueprint('shifts', __name__)

@shifts_bp.route('', methods=['GET'])
def get_all_shifts():
    try:
        status = request.args.get('status')
        shift_obj = Shift()
        all_shifts = shift_obj.get_all_shifts(status)
        resp = [ShiftResponse(**s).dict() for s in all_shifts]
        return jsonify(resp), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error."}), HTTPStatus.INTERNAL_SERVER_ERROR

@shifts_bp.route('/worker/<worker_id>', methods=['GET'])
def get_shifts_by_worker(worker_id):
    try:
        status = request.args.get('status')
        shift_obj = Shift()
        user_shifts = shift_obj.get_shifts_by_worker(worker_id, status)
        resp = [ShiftResponse(**s).dict() for s in user_shifts]
        return jsonify(resp), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg == DB_USER_NOT_FOUND:
            return jsonify({'message': "Worker not found."}), HTTPStatus.NOT_FOUND
        elif msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error."}), HTTPStatus.INTERNAL_SERVER_ERROR

@shifts_bp.route('', methods=['POST'])
def add_shift():
    try:
        data = ShiftRequest(**request.get_json())
        shift_obj = Shift().create_shift(data.dict())
        resp = ShiftResponse(**shift_obj.to_dict()).dict()
        return jsonify(resp), HTTPStatus.CREATED
    except ValidationError:
        return jsonify({'message': INVALID_INPUT_DATA}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        msg = str(e)
        if msg == DB_USER_NOT_FOUND:
            return jsonify({'message': "Worker not found."}), HTTPStatus.NOT_FOUND
        elif msg == "Only workers can be assigned shifts":
            return jsonify({'message': msg}), HTTPStatus.BAD_REQUEST
        elif msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error."}), HTTPStatus.INTERNAL_SERVER_ERROR

@shifts_bp.route('/<shift_id>/approve', methods=['PUT'])
def approve_shift(shift_id):
    try:
        shift_obj = Shift()
        shift_obj.approve_shift(shift_id)
        return jsonify({'message': 'Shift approved successfully'}), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg == "Shift not found":
            return jsonify({'message': msg}), HTTPStatus.NOT_FOUND
        elif msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error."}), HTTPStatus.INTERNAL_SERVER_ERROR

@shifts_bp.route('/<shift_id>/deny', methods=['PUT'])
def deny_shift(shift_id):
    try:
        shift_obj = Shift()
        shift_obj.deny_shift(shift_id)
        return jsonify({'message': 'Shift denied successfully'}), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg == "Shift not found":
            return jsonify({'message': msg}), HTTPStatus.NOT_FOUND
        elif msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error."}), HTTPStatus.INTERNAL_SERVER_ERROR

@shifts_bp.route('/<shift_id>', methods=['DELETE'])
def delete_shift(shift_id):
    try:
        shift_obj = Shift()
        shift_obj.delete_shift(shift_id)
        return jsonify({'message': 'Shift deleted successfully'}), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg == "Shift not found":
            return jsonify({'message': msg}), HTTPStatus.NOT_FOUND
        elif msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error."}), HTTPStatus.INTERNAL_SERVER_ERROR
