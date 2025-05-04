import json
from common.status import status as st
from src.utils.response import ok, fail
from dal.hardware import HardwareDAL
from common.errors import ErrorMessage as EM

_dal = HardwareDAL()

def create_hardware(event, _):
    _dal.create(json.loads(event["body"]))
    return ok({"message": "created"}, st.CREATED)

def list_hardware(_e, _):
    return ok(_dal.list())

def get_hardware(event, _):
    try:
        return ok(_dal.get(event["pathParameters"]["hw_id"]))
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)

def update_hardware(event, _):
    try:
        _dal.update(event["pathParameters"]["hw_id"], json.loads(event["body"]))
        return ok({"message": "updated"})
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)

def delete_hardware(event, _):
    try:
        _dal.delete(event["pathParameters"]["hw_id"])
        return ok({}, st.NO_CONTENT)
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)
