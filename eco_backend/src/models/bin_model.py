from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, String, Float
from src.models.db import Base
from enum import Enum

class BinStatus(str, Enum):
    Full = "Full"
    Mid = "Mid"
    Empty = "Empty"

class BinCreate(BaseModel):
    location: str
    address: str
    status: BinStatus = BinStatus.Empty
    lat: float
    lon: float
    capacity: float = 0.0

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            BinStatus: lambda v: v.value
        }
    )

class BinResponse(BaseModel):
    binId: str
    location: str
    address: str
    status: str
    lat: float
    lon: float
    capacity: float

    model_config = ConfigDict(
        from_attributes=True
    )

class Bin(Base):
    __tablename__ = "bins"

    binId = Column(String(50), primary_key=True)
    location = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    status = Column(String, nullable=False, default=BinStatus.Empty)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    capacity = Column(Float, nullable=False, default=0.0)
