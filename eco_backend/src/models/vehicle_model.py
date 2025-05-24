from pydantic import BaseModel, constr
from datetime import date
from sqlalchemy import Column, String, Date
from src.models.db import Base

class VehicleBase(BaseModel):
    type: str
    status: str
    location: str
    lastMaintenance: date

class VehicleCreate(VehicleBase):
    licensePlate: constr(min_length=1, max_length=20)

class VehicleOut(VehicleBase):
    licensePlate: constr(min_length=1, max_length=20)
    type: str
    status: str
    location: str
    lastMaintenance: date
    
    class Config:
        from_attributes = True

class Vehicle(Base):
    __tablename__ = "vehicles"

    licensePlate = Column(String(20), primary_key=True, unique=True, nullable=False)
    type = Column(String(50), nullable=False)
    status = Column(String(30), nullable=False)
    location = Column(String(100), nullable=False)
    lastMaintenance = Column(Date, nullable=False)