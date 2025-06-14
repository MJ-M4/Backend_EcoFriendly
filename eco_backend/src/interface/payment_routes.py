from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.datalayer.payment_data import create_payment, fetch_all_payments, fetch_payments_by_worker, update_payment, delete_payment
from src.models.payment_model import PaymentCreate, PaymentUpdate
from src.errors.general_errors import DataFetchError

payment_bp = Blueprint("payments", __name__)

@payment_bp.route("/getPayments", methods=["GET"])
def get_payments():
    try:
        payments = fetch_all_payments()
        return jsonify({"status": "success", "payments": payments}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@payment_bp.route("/addPayment", methods=["POST"])
def add_payment():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), HTTPStatus.BAD_REQUEST
        payment_data = PaymentCreate.model_validate(data)
        result = create_payment(payment_data)
        return jsonify({"status": "success", "message": "Payment added", "payment": result}), HTTPStatus.CREATED
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR


@payment_bp.route("/updatePayment/<payment_id>", methods=["PUT"])
def update_payment_route(payment_id: str):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), HTTPStatus.BAD_REQUEST
        payment_data = PaymentUpdate.model_validate(data)
        result = update_payment(payment_id, payment_data)
        return jsonify({"status": "success", "message": "Payment updated", "payment": result}), HTTPStatus.OK
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), HTTPStatus.BAD_REQUEST
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@payment_bp.route("/deletePayment/<payment_id>", methods=["DELETE"])
def delete_payment_route(payment_id: str):
    try:
        delete_payment(payment_id)
        return jsonify({"status": "success", "message":"Payment deleted"}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    
@payment_bp.route("/getMyPayments/<worker_id>", methods=["GET"])
def get_my_payments(worker_id: str):
    try:
        payments = fetch_payments_by_worker(worker_id)
        return jsonify({"status": "success", "payments": payments}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR