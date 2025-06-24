import uuid
from sqlalchemy.orm import Session
from src.models.db import SessionLocal
from src.models.hardware_model import Hardware, HardwareCreate, HardwareOut, HardwareStatus
from src.errors.general_errors import DataFetchError

def fetch_all_hardware():
    session: Session = SessionLocal()
    try:
        hardware = session.query(Hardware).all()
        return [HardwareOut.model_validate(hw).model_dump() for hw in hardware]
    except Exception as e:
        raise DataFetchError(f"[Error fetching hardware] {str(e)}")
    finally:
        session.close()

def add_hardware(hw: HardwareCreate):
    session: Session = SessionLocal()
    try:
        status = (
            HardwareStatus.NeedsMaintenance
            if hw.battery < 40
            else HardwareStatus.Operational
        )
        new_hw = Hardware(
            id=str(uuid.uuid4())[:8],
            binId=hw.binId,
            status=status,
            battery=hw.battery,
            lastChecked=hw.lastChecked
        )
        session.add(new_hw)
        session.commit()
        session.refresh(new_hw)
        return HardwareOut.model_validate(new_hw).model_dump()
    except Exception as e:
        session.rollback()
        raise DataFetchError(
            f"Cannot add hardware: Bin ID '{hw.binId}' does not exist. Please make sure to add the bin first."
        )
    finally:
        session.close()

def delete_hardware_by_id(hw_id: str):
    session: Session = SessionLocal()
    try:
        hw = session.query(Hardware).filter_by(id=hw_id).first()
        if not hw:
            raise DataFetchError("Hardware not found.")
        session.delete(hw)
        session.commit()
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error deleting hardware] {str(e)}")
    finally:
        session.close()


def update_hardware_status(hw_id: str, new_status: str, new_battery: float):
    session: Session = SessionLocal()
    try:
        hw = session.query(Hardware).filter_by(id=hw_id).first()
        if not hw:
            raise DataFetchError("Hardware not found.")
        # Status is auto set
        status = (
            HardwareStatus.NeedsMaintenance
            if new_battery < 40
            else HardwareStatus.Operational
        )
        hw.status = status
        hw.battery = new_battery
        session.commit()
        return HardwareOut.model_validate(hw).model_dump()
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error updating hardware] {str(e)}")
    finally:
        session.close()
