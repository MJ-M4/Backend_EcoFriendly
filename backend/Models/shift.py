from datetime import date, time
from pydantic import BaseModel as _Schema, Field
from Backend_EcoFriendly.backend.Models.base import BaseModel

class ShiftSchema(_Schema):
    worker_id:   str
    worker_name: str
    worker_type: str | None = None
    date:        date
    start_time:  time
    end_time:    time
    location:    str
    status:      str = "pending"

class Shift(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self._schema = ShiftSchema(**kwargs)

    def to_dict(self):
        return self._schema.model_dump()