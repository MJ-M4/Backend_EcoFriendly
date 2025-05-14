"""Re-export every domain model for convenient star-imports."""
from .role import Role
from .user import User
from .bin import Bin
from .bin_reading import BinReading
from .vehicle import Vehicle
from .shift import Shift
from .payroll import Payroll

__all__ = [
    "Role",
    "User",
    "Bin",
    "BinReading",
    "Vehicle",
    "Shift",
    "Payroll",
]