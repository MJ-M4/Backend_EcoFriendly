from pydantic import BaseModel, ConfigDict
from typing import Any
from pydantic_core import core_schema
from sqlalchemy import Column, String,Enum
from src.models.db import Base
from enum import Enum

class BinStatus(str, Enum):
    Full = "Full"
    Mid = "Mid"
    Empty = "Empty"

    @classmethod
    def __get_pydantic_core_schema__(
        cls, 
        _source_type: Any,
        _handler: Any,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            lambda x: cls(x) if isinstance(x, str) else x,
        )

class BinCreate(BaseModel):
    location: str
    address: str
    status: BinStatus = BinStatus.Empty
    
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
    status: str  # غيرنا من BinStatus إلى str مباشرة
    
    model_config = ConfigDict(
        from_attributes=True
    )
 
class Bin(Base):
    __tablename__ = "bins"

    binId = Column(String(50), primary_key=True)
    location = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    status = Column(String, nullable=False, default=BinStatus.Empty)



