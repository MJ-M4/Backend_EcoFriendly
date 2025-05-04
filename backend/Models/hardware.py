from datetime import date
from pydantic import BaseModel as _Schema, Field
from Backend_EcoFriendly.backend.Models.base import BaseModel

class HardwareSchema(_Schema):
    id:           str = Field(..., min_length=1)
    bin_id:       str
    status:       str = "Operational"
    battery:      int = Field(ge=0, le=100, default=100)
    last_checked: date | None = None
    location:     str | None = None
    address:      str | None = None

class Hardware(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self._schema = HardwareSchema(**kwargs)

    def to_dict(self):
        return self._schema.model_dump()