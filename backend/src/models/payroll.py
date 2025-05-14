from typing import Optional
from datetime import date

from pydantic import BaseModel, ConfigDict, field_validator


class Payroll(BaseModel):
    payroll_id: Optional[int] = None
    employee_id: int
    month: int  # YYYYMM, e.g., 202501
    amount_nis: float
    paid: bool = False

    model_config = ConfigDict(from_attributes=True)

    @field_validator("month")
    @classmethod
    def _yyyymm(cls, v: int) -> int:
        if v < 190001 or v > 210012:
            raise ValueError("month field expects YYYYMM integer")
        return v