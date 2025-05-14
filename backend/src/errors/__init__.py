"""
Centralised textual error catalogue.

All error identifiers are UPPER_SNAKE_CASE strings.
No numeric codes are exposed to callers or hard-coded in this file.
"""
from enum import Enum


class ErrorMessage(str, Enum):
    # ────────────────────────── Generic / shared ───────────────────────────
    DB_ERROR = "DB_ERROR"
    PERMISSION_DENIED = "PERMISSION_DENIED"

    # ───────────────────────────── Auth / Users ────────────────────────────
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    USER_NOT_FOUND = "USER_NOT_FOUND"

    # ───────────────────────────── Domain data ─────────────────────────────
    BIN_NOT_FOUND = "BIN_NOT_FOUND"
    VEHICLE_NOT_FOUND = "VEHICLE_NOT_FOUND"
    SHIFT_NOT_FOUND = "SHIFT_NOT_FOUND"
    PAYROLL_NOT_FOUND = "PAYROLL_NOT_FOUND"