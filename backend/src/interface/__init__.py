from importlib import import_module
from flask import Blueprint, Flask

_BLUEPRINTS = [
    "auth",
    "users",
    "bins",
    "vehicles",
    "shifts",
    "payroll",
    "reports",
]

def register_blueprints(app: Flask) -> None:
    """Auto-import and attach every blueprint in _BLUEPRINTS."""
    for name in _BLUEPRINTS:
        mod = import_module(f"src.interface.{name}")
        if hasattr(mod, "bp") and isinstance(mod.bp, Blueprint):
            app.register_blueprint(mod.bp, url_prefix="/api")
