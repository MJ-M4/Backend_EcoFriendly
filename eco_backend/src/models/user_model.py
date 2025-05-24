from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Date, DateTime
from src.models.db import Base

# ----------------- Pydantic Models -----------------
class UserResponse(BaseModel):
    identity: str
    name: str
    role: str
    worker_type: Optional[str] = None
    class Config:
        from_attributes = True

class LoginInput(BaseModel):
    identity: str = Field(..., min_length=5, max_length=20)
    password: str = Field(..., min_length=6)

class EmployeeCreate(BaseModel):
    identity: str
    name: str
    phone: str
    location: str
    joining_date: date
    role: str
    worker_type: str
    password: str

class EmployeeOut(BaseModel):
    identity: str
    name: str
    phone: str
    location: str
    joining_date: date
    role: str
    worker_type: Optional[str] = None

    class Config:
        from_attributes = True

# ----------------- SQLAlchemy ORM -----------------
class EmployeeORM(Base):
    __tablename__ = "employees"
    
    identity = Column(String(20),primary_key=True, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    location = Column(String(100))
    joining_date = Column(Date)
    role = Column(String(20), nullable=False)
    worker_type = Column(String(50))
    created_at = Column(DateTime, nullable=False)
    hashed_password = Column(String(256), nullable=False)
