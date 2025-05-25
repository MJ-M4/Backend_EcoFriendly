import uuid
from sqlalchemy.orm import Session
from src.models.db import SessionLocal
from src.errors.general_errors import DataFetchError
from src.models.bin_model import Bin,BinResponse,BinCreate


def fetch_all_bins():
    session: Session = SessionLocal()
    try:
        bins = session.query(Bin).all()
        return [{
            "binId": bin.binId,
            "location": bin.location,
            "address": bin.address,
            "status": bin.status  
        } for bin in bins]
    except Exception as e:
        raise DataFetchError(f"[Error fetching bins] {str(e)}")
    finally:
        session.close()

def add_bin(bin: BinCreate):
    session: Session = SessionLocal()
    try:
        new_bin = Bin(
            binId=str(uuid.uuid4())[:5],
            location=bin.location,
            address=bin.address,
            status=bin.status
        )
        session.add(new_bin)
        session.commit()
        session.refresh(new_bin)
        return {
            "binId": new_bin.binId,
            "location": new_bin.location,
            "address": new_bin.address,
            "status": new_bin.status  # استخدم .value هنا للاستجابة
        }
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error adding bin] {str(e)}")
    finally:
        session.close()

def delete_bin_by_id(binId: str):
    session: Session = SessionLocal()
    try:
        bin = session.query(Bin).filter_by(binId=binId).first()
        if not bin:
            raise DataFetchError("Bin not found.")
        session.delete(bin)
        session.commit()
        return {"message": "Bin deleted successfully."}
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error deleting bin] {str(e)}")
    finally:
        session.close()
