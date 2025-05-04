class ErrorMessage(str):
    """Human‑readable, single‑source error constants."""
    DB_CONNECTION_FAILED    = "Database connection failed."
    QUERY_FAILED            = "Database query failed."

    USER_EXISTS             = "User already exists."
    USER_NOT_FOUND          = "User not found."
    INVALID_CREDENTIALS     = "Invalid ID / password."

    PAYMENT_NOT_FOUND       = "Payment not found."
    SHIFT_NOT_FOUND         = "Shift not found."
    BIN_NOT_FOUND           = "Bin not found."
    VEHICLE_NOT_FOUND       = "Vehicle not found."
    HARDWARE_NOT_FOUND      = "Hardware not found."