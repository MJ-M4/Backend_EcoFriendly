from flask import Blueprint, request, jsonify, make_response
from Models.Payment import Payment
from pydantic import BaseModel, ValidationError
from http import HTTPStatus
from datetime import datetime

payments_bp = Blueprint('payments', __name__)

class PaymentModel(BaseModel):
    worker_id: int
    amount: float
    payment_date: str = None
    status: str
    notes: str = None

@payments_bp.route('/', methods=['GET'])
def get_payments():
    payments = Payment.get_all()
    return make_response(jsonify([p.to_dict() for p in payments]), HTTPStatus.OK)

@payments_bp.route('/', methods=['POST'])
def add_payment():
    try:
        data = PaymentModel(**request.get_json())
    except ValidationError as e:
        return make_response(jsonify({'error': e.errors()}), HTTPStatus.BAD_REQUEST)
    
    payment_date = datetime.fromisoformat(data.payment_date).date() if data.payment_date else None
    new_payment = Payment.create(
        worker_id=data.worker_id,
        amount=data.amount,
        payment_date=payment_date,
        status=data.status,
        notes=data.notes
    )
    return make_response(jsonify(new_payment.to_dict()), HTTPStatus.CREATED)

@payments_bp.route('/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return make_response(jsonify({'error': 'Payment not found'}), HTTPStatus.NOT_FOUND)
    
    payment.status = 'Paid'
    payment.payment_date = datetime.now().date()
    db.session.commit()
    return make_response(jsonify(payment.to_dict()), HTTPStatus.OK)