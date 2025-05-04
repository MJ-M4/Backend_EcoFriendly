# backend/Models/bin.py
from pydantic import BaseModel as _Schema, Field
from datetime import datetime
from Models.base import BaseModel

class BinSchema(_Schema):
    bin_id:   str   = Field(..., min_length=1)
    location: str   = ""
    address:  str   | None = None
    status:   str   = "Empty"          # 'Empty' | 'Near Full' | 'Full'
    capacity: int   = 0                # 0‑100
    route:    str   | None = None
    battery:  int   = 100              # 0‑100
    lat:      float | None = None
    lon:      float | None = None
    updated_at: datetime | None = None

class Bin(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self._schema = BinSchema(**kwargs)

    def to_dict(self):
        return self._schema.model_dump()
