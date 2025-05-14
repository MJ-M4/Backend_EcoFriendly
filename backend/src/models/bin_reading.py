from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class BinReading(BaseModel):
    reading_id: Optional[int] = None
    bin_id: int
    level_pct: int  # 0-100
    ts: datetime = datetime.utcnow()

    model_config = ConfigDict(from_attributes=True)

    # ─────────────── validation ───────────────
    @field_validator("level_pct")
    @classmethod
    def _0_to_100(cls, v: int) -> int:
        if not 0 <= v <= 100:
            raise ValueError("level_pct must be between 0 and 100")
        return v
