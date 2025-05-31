from sqlalchemy import Column, String, Time, Date, Enum, ForeignKey
from src.models.db import Base
from pydantic import BaseModel
from datetime import date,time
import enum

class ProposalStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"


class ShiftProposalCreate(BaseModel):
    worker_id: str
    worker_name: str
    worker_type: str
    date: date
    start_time: time
    end_time: time
    location: str

class ShiftProposalOut(BaseModel):
    id: str
    worker_id: str
    worker_name: str
    worker_type: str
    submitted_at: date
    date: date
    start_time: time
    end_time: time
    location: str
    status: str


    class Config:
        from_attributes = True



class ShiftProposal(Base):
    __tablename__ = "shift_proposals"

    id = Column(String, primary_key=True)
    worker_id = Column(String(20), ForeignKey("employees.identity"), nullable=False)
    worker_name = Column(String(100), nullable=False)
    worker_type = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    location = Column(String(100), nullable=False)
    status = Column(Enum(ProposalStatus), nullable=False, default=ProposalStatus.PENDING)
    submitted_at = Column(Date, nullable=False)