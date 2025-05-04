from src.utils.response import ok
from dal.hardware import HardwareDAL

_hdl = HardwareDAL()

def list_alerts(_event, _ctx):
    return ok(_hdl.alerts())