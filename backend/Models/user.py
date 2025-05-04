from datetime import date
from pydantic import BaseModel as _Schema, Field
from Backend_EcoFriendly.backend.Models.base import BaseModel

class UserSchema(_Schema):
    user_id:     str = Field(..., min_length=1)
    name:        str
    password:    str = Field(..., min_length=8)
    role:        str = "worker"
    phone:       str | None = None
    location:    str | None = None
    joining_date:date | None = None
    worker_type: str | None = None

class User(BaseModel):
    def __init__(self, **kwargs):
        super().__init__()
        self._schema = UserSchema(**kwargs)

    def to_dict(self):
        data = self._schema.model_dump()
        data.pop("password", None)  # never expose hash from business object
        return data