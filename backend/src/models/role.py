from enum import Enum
from pydantic import BaseModel, ConfigDict


class RoleName(str, Enum):
    MANAGER = "manager"
    EMPLOYEE = "employee"


class Role(BaseModel):
    role_id: int | None = None
    role_name: RoleName

    model_config = ConfigDict(from_attributes=True)