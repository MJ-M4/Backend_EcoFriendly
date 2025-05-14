from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class Shift(BaseModel):
    shift_id: Optional[int] = None
    employee_id: int
    start_ts: datetime
    end_ts: datetime
    approved_by: Optional[int] = None  # manager ID

    model_config = ConfigDict(from_attributes=True)

    # guarantee logical time range
    @field_validator("end_ts")
    @classmethod
    def _after_start(cls, v: datetime, info):  # noqa: N805
        if v <= info.data["start_ts"]:
            raise ValueError("end_ts must be after start_ts")
        return v