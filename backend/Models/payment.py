from datetime import date
from pydantic import BaseModel as _Schema, Field
from Backend_EcoFriendly.backend.Models.base import BaseModel

class PaymentSchema(_Schema):
    worker_id:   str  = Field(..., min_length=1)
    worker_name: str
    amount:      float = Field(..., gt=0)
    payment_date:date
    status:      str  = "Pending"
    notes:       str | None = None

class Payment(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self._schema = PaymentSchema(**kwargs)

    def to_dict(self):
        return self._schema.model_dump()