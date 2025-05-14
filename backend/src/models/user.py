import bcrypt
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from .role import RoleName


class User(BaseModel):
    user_id: int
    role_id: int
    first_name: str
    last_name: str
    password_hash: str
    is_active: bool = True
    created_at: datetime = datetime.utcnow()

    # ──────────────── Pydantic settings ────────────────
    model_config = ConfigDict(from_attributes=True)

    # ──────────────── Validators / setters ─────────────
    @field_validator("password_hash", mode="before")
    @classmethod
    def _ensure_hash(cls, v: str | bytes) -> str:
        """Accept raw passwords and auto-hash them; keep existing hashes as-is."""
        if isinstance(v, bytes):
            v = v.decode()
        if v.startswith("$2b$") or v.startswith("$2a$"):
            return v  # looks like bcrypt
        return bcrypt.hashpw(v.encode(), bcrypt.gensalt()).decode()

    # ──────────────── Convenience getters ──────────────
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def check_password(self, raw_pw: str) -> bool:
        return bcrypt.checkpw(raw_pw.encode(), self.password_hash.encode())

    def is_manager(self) -> bool:
        return self.role_id == 1  # maps to RoleName.MANAGER

    # ↪ No numeric literals appear elsewhere in the codebase!