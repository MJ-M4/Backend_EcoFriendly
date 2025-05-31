import uuid
from sqlalchemy.orm import Session
from src.models.db import SessionLocal
from src.errors.general_errors import DataFetchError
from src.models.shift_model import Shift, ShiftCreate , ShiftUpdate

def fetch_all_shifts():
    session: Session = SessionLocal()
    try:
        shifts = session.query(Shift).all()
        return [{
            "shift_id": shift.shift_id,
            "worker_id": shift.worker_id,
            "worker_name": shift.worker_name,
            "worker_type": shift.worker_type,
            "date": shift.date.isoformat() if shift.date else None,
            "start_time": shift.start_time.isoformat() if shift.start_time else None,
            "end_time": shift.end_time.isoformat() if shift.end_time else None,
            "location": shift.location,
        } for shift in shifts]
    except Exception as e:
        raise DataFetchError(f"[Error fetching shifts] {str(e)}")
    finally:
        session.close()

def add_shift(shift: ShiftCreate):
    session: Session = SessionLocal()
    try:
        new_shift = Shift(
            shift_id=str(uuid.uuid4())[:5],
            worker_id=shift.worker_id,
            worker_name=shift.worker_name,
            worker_type=shift.worker_type,
            date=shift.date,
            start_time=shift.start_time,
            end_time=shift.end_time,
            location=shift.location,
        )
        session.add(new_shift)
        session.commit()
        session.refresh(new_shift)
        return {
            "shift_id": new_shift.shift_id,
            "worker_id": new_shift.worker_id,
            "worker_name": new_shift.worker_name,
            "worker_type": new_shift.worker_type,
            "date": shift.date.isoformat() if shift.date else None,
            "start_time": shift.start_time.isoformat() if shift.start_time else None,
            "end_time": shift.end_time.isoformat() if shift.end_time else None,
            "location": new_shift.location,
        }
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error adding shift] {str(e)}")
    finally:
        session.close()

def delete_shift_by_id(shift_id: str):
    session: Session = SessionLocal()
    try:
        shift = session.query(Shift).filter_by(shift_id=shift_id).first()
        if not shift:
            raise DataFetchError("Shift not found.")
        session.delete(shift)
        session.commit()
        return {"message": "Shift deleted successfully."}
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error deleting shift] {str(e)}")
    finally:
        session.close()


def update_shift(shift_id: str, shift_data: ShiftUpdate):
    session: Session = SessionLocal()
    try:
        shift = session.query(Shift).filter_by(shift_id=shift_id).first()
        if not shift:
            raise DataFetchError("Shift not found.")
        shift.date = shift_data.date
        shift.start_time = shift_data.start_time
        shift.end_time = shift_data.end_time
        shift.location = shift_data.location
        session.commit()
        session.refresh(shift)
        return {
            "shift_id": shift.shift_id,
            "worker_id": shift.worker_id,
            "worker_name": shift.worker_name,
            "worker_type": shift.worker_type,
            "date": shift.date.isoformat(),
            "start_time": shift.start_time.isoformat(),
            "end_time": shift.end_time.isoformat(),
            "location": shift.location,
        }
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error updating shift] {str(e)}")
    finally:
        session.close()

