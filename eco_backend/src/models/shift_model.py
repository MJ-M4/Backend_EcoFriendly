from datetime import date,time
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column,String, Time, Date, ForeignKey
from src.models.db import Base


class ShiftBase(BaseModel):
    worker_id: str
    worker_name: str
    worker_type: str
    date: date
    start_time: time
    end_time: time
    location: str

    

class ShiftCreate(ShiftBase):
    pass

class ShiftUpdate(BaseModel):
    date: date
    start_time: time
    end_time: time
    location: str

class ShiftOut(ShiftBase):
    shift_id: str

    model_config = ConfigDict(
        from_attributes=True
    )



class Shift(Base):
    __tablename__ = "shifts"

    shift_id = Column(String(20), primary_key=True)
    worker_id = Column(String(20), ForeignKey("employees.identity"), nullable=False)
    worker_name = Column(String(100), nullable=False)
    worker_type = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    location = Column(String(100), nullable=False)
