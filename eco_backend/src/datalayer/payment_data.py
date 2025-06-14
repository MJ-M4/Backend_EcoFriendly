import uuid
from sqlalchemy.orm import Session
from src.models.db import SessionLocal
from src.errors.general_errors import DataFetchError
from src.models.payment_model import Payment, PaymentCreate, PaymentUpdate, PaymentStatus
from datetime import datetime

def fetch_all_payments():
    session: Session = SessionLocal()
    try:
        payments = session.query(Payment).all()
        return [{
            "payment_id": payment.payment_id,
            "worker_id": payment.worker_id,
            "worker_name": payment.worker_name,
            "amount": payment.amount,
            "payment_date": payment.payment_date.isoformat() if payment.payment_date else None,
            "status": payment.status.value,
            "notes": payment.notes
        } for payment in payments]
    except Exception as e:
        raise DataFetchError(f"[Error fetching payments] {str(e)}")
    finally:
        session.close()

def create_payment(payment: PaymentCreate):
    session: Session = SessionLocal()
    try:
        new_payment = Payment(
            payment_id=str(uuid.uuid4())[:5],
            worker_id=payment.worker_id,
            worker_name=payment.worker_name,
            amount=payment.amount,
            payment_date=payment.payment_date.isoformat() if payment.payment_date else None,
            status=PaymentStatus.PENDING,
            notes=payment.notes
        )
        session.add(new_payment)
        session.commit()
        session.refresh(new_payment)
        return [{
            "payment_id": new_payment.payment_id,
            "worker_id": new_payment.worker_id,
            "worker_name": new_payment.worker_name,
            "amount": new_payment.amount,
            "payment_date": new_payment.payment_date.isoformat() if new_payment.payment_date else None,
            "status": new_payment.status.value,
            "notes": new_payment.notes
        }]
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error creating payment] {str(e)}")
    finally:
        session.close()

def update_payment(payment_id: str, payment_data: PaymentUpdate):
    session: Session = SessionLocal()
    try:
        payment = session.query(Payment).filter_by(payment_id=payment_id).first()
        if not payment:
            raise DataFetchError("Payment not found.")
        payment.status = PaymentStatus(payment_data.status)
        payment.payment_date = payment.payment_date.isoformat() if payment.payment_date else None
        session.commit()
        session.refresh(payment)
        return [{
            "payment_id": payment.payment_id,
            "worker_id": payment.worker_id,
            "worker_name": payment.worker_name,
            "amount": payment.amount,
            "payment_date": payment.payment_date.isoformat() if payment.payment_date else None,
            "status": payment.status.value,
            "notes": payment.notes
        }]
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error updating payment] {str(e)}")
    finally:
        session.close()

def delete_payment(payment_id: str):
    session: Session = SessionLocal()
    try:
        payment = session.query(Payment).filter_by(payment_id=payment_id).first()
        if not payment:
            raise DataFetchError("Payment not found.")
        session.delete(payment)
        session.commit()
        return {"message": "Payment deleted successfully."}
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error deleting payment] {str(e)}")
    finally:
        session.close()

def fetch_payments_by_worker(worker_id: str):
    session: Session = SessionLocal()
    try:
        payments = session.query(Payment).filter_by(worker_id=worker_id).all()
        return [{
            "payment_id": payment.payment_id,
            "worker_id": payment.worker_id,
            "worker_name": payment.worker_name,
            "amount": payment.amount,
            "payment_date": payment.payment_date.isoformat() if payment.payment_date else None,
            "status": payment.status.value,
            "notes": payment.notes
        } for payment in payments]
    except Exception as e:
        raise DataFetchError(f"[Error fetching payments for worker] {str(e)}")
    finally:
        session.close()