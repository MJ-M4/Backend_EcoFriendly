from flask import Blueprint, request, jsonify
from flask_backend.model import db, Payment, User
from datetime import datetime
import logging

payments_bp = Blueprint('payments', __name__)
logger = logging.getLogger(__name__)

@payments_bp.route('/', methods=['GET'])
def get_payments():
    logger.debug("GET /payments -> get_payments")
    payments = Payment.query.all()
    return jsonify([{
        "id": p.id,
        "workerId": str(User.query.get(p.worker_id).identity),  # Use identity instead of numeric_id
        "workerName": User.query.get(p.worker_id).name,
        "amount": float(p.amount),
        "paymentDate": p.payment_date.isoformat() if p.payment_date else '',
        "status": p.status,
        "notes": p.notes or ''
    } for p in payments]), 200

@payments_bp.route('/', methods=['POST'])
def add_payment():
    logger.debug("POST /payments -> add_payment")
    data = request.get_json() or {}
    logger.debug(f"Request JSON: {data}")

    required = ["workerId", "amount"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # Find worker by identity (convert to int since it's BigInteger)
    worker = User.query.filter_by(identity=int(data["workerId"])).first()
    if not worker:
        return jsonify({"error": "Invalid Worker ID. Worker not found."}), 404

    try:
        amount = float(data["amount"])
        if amount <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400

        new_payment = Payment(
            worker_id=worker.id,
            amount=amount,
            payment_date=None,
            status="Pending",
            notes=data.get("notes", "")
        )
        db.session.add(new_payment)
        db.session.commit()
        return jsonify({
            "message": "Payment added successfully",
            "id": new_payment.id,
            "workerId": str(worker.identity),  # Use identity instead of numeric_id
            "workerName": worker.name,
            "amount": float(new_payment.amount),
            "paymentDate": '',
            "status": new_payment.status,
            "notes": new_payment.notes
        }), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": "Invalid amount format", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding payment: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@payments_bp.route('/<int:id>', methods=['PUT'])
def update_payment(id):
    logger.debug(f"PUT /payments/{id} -> update_payment")
    payment = Payment.query.get(id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    data = request.get_json() or {}
    logger.debug(f"Request JSON: {data}")

    if "status" not in data:
        return jsonify({"error": "Status field is required"}), 400

    if data["status"] not in ["Pending", "Paid"]:
        return jsonify({"error": "Status must be 'Pending' or 'Paid'"}), 400

    try:
        payment.status = data["status"]
        if payment.status == "Paid" and not payment.payment_date:
            payment.payment_date = datetime.now().date()
        elif payment.status == "Pending":
            payment.payment_date = None
        db.session.commit()
        worker = User.query.get(payment.worker_id)
        return jsonify({
            "message": "Payment updated successfully",
            "id": payment.id,
            "workerId": str(worker.identity),  # Use identity instead of numeric_id
            "workerName": worker.name,
            "amount": float(payment.amount),
            "paymentDate": payment.payment_date.isoformat() if payment.payment_date else '',
            "status": payment.status,
            "notes": payment.notes
        }), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating payment: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@payments_bp.route('/<int:id>', methods=['DELETE'])
def delete_payment(id):
    logger.debug(f"DELETE /payments/{id} -> delete_payment")
    payment = Payment.query.get(id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    try:
        db.session.delete(payment)
        db.session.commit()
        return jsonify({"message": "Payment deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting payment: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500