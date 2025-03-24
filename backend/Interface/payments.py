# backend/Interface/payments.py
from flask import Blueprint, request, jsonify
from pydantic import BaseModel, Field, ValidationError, confloat
from typing import Optional, Literal
from http import HTTPStatus

from Models.payment import Payment
from DataLayer.errors import (
    INVALID_INPUT_DATA,
    DB_CONNECTION_ERROR,
    DB_QUERY_ERROR
)

payments_bp = Blueprint('payments', __name__)

class PaymentRequest(BaseModel):
    worker_id: str = Field(..., min_length=1, description="Worker ID")
    worker_name: str = Field(..., min_length=1, description="Worker name")
    amount: float = Field(..., gt=0, description="Amount must be positive")
    payment_date: str = Field(..., description="YYYY-MM-DD format")
    status: Literal['Pending','Paid'] = 'Pending'
    notes: str = Field(..., min_length=1, description="Notes about the payment")

class PaymentResponse(BaseModel):
    id: int
    worker_id: str
    worker_name: str
    amount: float
    payment_date: str
    status: Literal['Pending','Paid']
    notes: Optional[str]

@payments_bp.route('', methods=['GET'])
def get_all_payments():
    """
    GET /api/payments
    """
    try:
        pay_obj = Payment()
        payments_list = pay_obj.get_all_payments()
        response_data = [PaymentResponse(**p).dict() for p in payments_list]
        return jsonify(response_data), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': "Unexpected error"}), HTTPStatus.INTERNAL_SERVER_ERROR

@payments_bp.route('', methods=['POST'])
def create_payment():
    """
    POST /api/payments
    {
      "worker_id": "207705096",
      "worker_name": "mhagne",
      "amount": 1500.0,
      "payment_date": "2025-03-01",
      "status": "Pending",
      "notes": "Monthly salary"
    }
    """
    try:
        data = PaymentRequest(**request.get_json())
        pay = Payment().create_payment(data.dict())
        resp = PaymentResponse(**pay.to_dict()).dict()
        return jsonify(resp), HTTPStatus.CREATED
    except ValidationError:
        return jsonify({'message': INVALID_INPUT_DATA}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        msg = str(e)
        if msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': msg}), HTTPStatus.BAD_REQUEST

@payments_bp.route('/<int:payment_id>/pay', methods=['PUT'])
def mark_payment_as_paid(payment_id):
    """
    PUT /api/payments/<payment_id>/pay?date=YYYY-MM-DD
    Optionally pass a new date in query param or request body
    """
    try:
        new_date = request.args.get('date')  # or read from JSON
        pay = Payment()
        pay.mark_as_paid(payment_id, new_date)
        return jsonify({'message': 'Payment marked as paid'}), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg == "Payment not found":
            return jsonify({'message': msg}), HTTPStatus.NOT_FOUND
        elif msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': msg}), HTTPStatus.BAD_REQUEST

@payments_bp.route('/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    """
    DELETE /api/payments/<payment_id>
    """
    try:
        pay = Payment()
        pay.delete_payment(payment_id)
        return jsonify({'message': 'Payment deleted successfully'}), HTTPStatus.OK
    except Exception as e:
        msg = str(e)
        if msg == "Payment not found":
            return jsonify({'message': msg}), HTTPStatus.NOT_FOUND
        elif msg in [DB_CONNECTION_ERROR, DB_QUERY_ERROR]:
            return jsonify({'message': msg}), HTTPStatus.SERVICE_UNAVAILABLE
        return jsonify({'message': msg}), HTTPStatus.BAD_REQUEST
