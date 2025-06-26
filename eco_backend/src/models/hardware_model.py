from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Float, Enum as SAEnum, ForeignKey
from src.models.db import Base
from enum import Enum as PyEnum

class HardwareStatus(str, PyEnum):
    Operational = "Operational"
    NeedsMaintenance = "Needs Maintenance"  # <-- Note the space!

class HardwareCreate(BaseModel):
    binId: str
    status: HardwareStatus = HardwareStatus.Operational
    battery: float = 100.0
    lastChecked: str

class HardwareOut(BaseModel):
    id: str
    binId: str
    status: HardwareStatus
    battery: float
    lastChecked: str

    class Config:
        from_attributes = True

class Hardware(Base):
    __tablename__ = "hardware"

    id = Column(String(50), primary_key=True, unique=True, nullable=False)
    binId = Column(String(50), ForeignKey('bins.binId'))
    status = Column(
        SAEnum(HardwareStatus, values_callable=lambda obj: [e.value for e in obj]),  # Ensures correct value stored
        nullable=False,
        default=HardwareStatus.Operational.value,  # <-- Use `.value` to ensure string not enum!
    )
    battery = Column(Float, nullable=False, default=100.0)
    lastChecked = Column(String(50), nullable=False)

    
    def __repr__(self):
        return f"<Hardware(id={self.id}, binId={self.binId}, status={self.status}, battery={self.battery}, lastChecked={self.lastChecked})>"
    def __str__(self):
        return f"Hardware ID: {self.id}, Bin ID: {self.binId}, Status: {self.status}, Battery: {self.battery}, Last Checked: {self.lastChecked}"
    def __hash__(self):
        return hash((self.id, self.binId, self.status, self.battery, self.lastChecked))
    def __eq__(self, other):
        if not isinstance(other, Hardware):
            return NotImplemented
        return (
            self.id == other.id and
            self.binId == other.binId and
            self.status == other.status and
            self.battery == other.battery and
            self.lastChecked == other.lastChecked
        )
    def __ne__(self, other):
        if not isinstance(other, Hardware):
            return NotImplemented
        return not self.__eq__(other)
    def __lt__(self, other):
        if not isinstance(other, Hardware):
            return NotImplemented
        return self.id < other.id
    def __le__(self, other):
        if not isinstance(other, Hardware):
            return NotImplemented
        return self.id <= other.id
    def __gt__(self, other):
        if not isinstance(other, Hardware):
            return NotImplemented
        return self.id > other.id                   