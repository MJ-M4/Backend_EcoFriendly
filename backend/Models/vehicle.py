from datetime import date
from pydantic import BaseModel as _Schema, Field
from Backend_EcoFriendly.backend.Models.base import BaseModel

class VehicleSchema(_Schema):
    type:             str
    license_plate:    str = Field(..., min_length=3)
    status:           str = "Available"
    location:         str | None = None
    last_maintenance: date | None = None

class Vehicle(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self._schema = VehicleSchema(**kwargs)

    def to_dict(self):
        return self._schema.model_dump()