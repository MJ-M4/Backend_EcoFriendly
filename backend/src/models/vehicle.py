from typing import Optional

from pydantic import BaseModel, ConfigDict


class Vehicle(BaseModel):
    vehicle_id: Optional[int] = None
    plate: str
    capacity_l: int

    model_config = ConfigDict(from_attributes=True)