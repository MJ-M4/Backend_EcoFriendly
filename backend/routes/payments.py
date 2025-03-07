# backend/routes/payments.py
from flask import Blueprint, request, jsonify
from extensions import db  # Import db from extensions.py
from models.payment import Payment

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return jsonify([{
        'id': payment.id,
        'worker_id': payment.worker_id,
        'worker_name': payment.worker.name,
        'amount': float(payment.amount),
        'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
        'status': payment.status,
        'notes': payment.notes
    } for payment in payments]), 200

@payments_bp.route('/', methods=['POST'])
def add_payment():
    data = request.get_json()
    payment = Payment(
        worker_id=data['worker_id'],
        amount=data['amount'],
        payment_date=data.get('payment_date'),
        status=data['status'],
        notes=data.get('notes')
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({'message': 'Payment added successfully'}), 201

@payments_bp.route('/<int:id>', methods=['PUT'])
def update_payment(id):
    data = request.get_json()
    payment = Payment.query.get_or_404(id)
    payment.status = data.get('status', payment.status)
    payment.payment_date = data.get('payment_date', payment.payment_date)
    db.session.commit()
    return jsonify({'message': 'Payment updated successfully'}), 200

@payments_bp.route('/<int:id>', methods=['DELETE'])
def delete_payment(id):
    payment = Payment.query.get_or_404(id)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted successfully'}), 200