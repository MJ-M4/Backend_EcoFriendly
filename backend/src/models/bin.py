from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class Bin(BaseModel):
    bin_id: Optional[int] = None
    location: str
    capacity_l: int
    last_emptied: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    # Provide a setter to update `last_emptied` only when level <= 20 %
    def mark_emptied(self) -> None:
        self.last_emptied = datetime.utcnow()