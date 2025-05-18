from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class LoginInput(BaseModel):
    identity: str = Field(..., min_length=5, max_length=20)
    password: str = Field(..., min_length=6)

class User:
    def __init__(
        self,
        user_id: int,
        identity: str,
        name: str,
        phone: Optional[str],
        location: Optional[str],
        joining_date: Optional[date],
        role: str,
        worker_type: Optional[str],
        created_at: datetime
    ):
        self._user_id = user_id
        self._identity = identity
        self._name = name
        self._phone = phone
        self._location = location
        self._joining_date = joining_date
        self._role = role
        self._worker_type = worker_type
        self._created_at = created_at

    def get_id(self): return self._user_id
    def get_identity(self): return self._identity
    def get_name(self): return self._name
    def get_phone(self): return self._phone
    def get_location(self): return self._location
    def get_joining_date(self): return self._joining_date
    def get_role(self): return self._role
    def get_worker_type(self): return self._worker_type
    def get_created_at(self): return self._created_at