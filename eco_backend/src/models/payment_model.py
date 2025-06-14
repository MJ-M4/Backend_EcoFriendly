from sqlalchemy import Column, String, Date, Float, Enum
from src.models.db import Base
from pydantic import BaseModel, ConfigDict
from datetime import date
import enum

class PaymentStatus(enum.Enum):
    PENDING = "Pending"
    PAID = "Paid"

class PaymentCreate(BaseModel):
    worker_id: str
    worker_name: str
    amount: float
    payment_date: date
    notes: str

class PaymentUpdate(BaseModel):
    status: str
    payment_date: str

class PaymentOut(BaseModel):
    payment_id: str
    worker_id: str
    worker_name: str
    amount: float
    payment_date: date
    status: str
    notes: str

    model_config = ConfigDict(
        from_attributes=True
    )

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(String, primary_key=True)
    worker_id = Column(String(20), nullable=False)
    worker_name = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    notes = Column(String(255))