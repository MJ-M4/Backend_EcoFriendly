from sqlalchemy.orm import Session
from src.models.db import SessionLocal
from src.errors.general_errors import DataFetchError
from src.models.vehicle_model import Vehicle, VehicleCreate, VehicleOut


def fetch_all_vehicles():
    session: Session = SessionLocal()
    try:
        vehicles = session.query(Vehicle).all()
        return [VehicleOut.model_validate(vehicle).model_dump() for vehicle in vehicles]
    except Exception as e:
        raise DataFetchError(f"[Error fetching vehicles] {str(e)}")
    finally:
        session.close()

def add_vehicle(vehicle: VehicleCreate):
    session: Session = SessionLocal()
    try:
        new_vehicle = Vehicle(
            licensePlate=vehicle.licensePlate,
            type=vehicle.type,
            status=vehicle.status,
            location=vehicle.location,
            lastMaintenance=vehicle.lastMaintenance
        )
        session.add(new_vehicle)
        session.commit()
        session.refresh(new_vehicle)
        return VehicleOut.model_validate(new_vehicle).model_dump()
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error adding vehicle] {str(e)}")
    finally:
        session.close()

def delete_vehicle_by_id(licensePlate: str):
    session: Session = SessionLocal()
    try:
        vehicle = session.query(Vehicle).filter_by(licensePlate=licensePlate).first()
        if not vehicle:
            raise DataFetchError("Vehicle not found.")
        session.delete(vehicle)
        session.commit()
        return {"message": "Vehicle deleted successfully."}
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error deleting vehicle] {str(e)}")
    finally:
        session.close()
  


        