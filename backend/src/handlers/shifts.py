import json
from common.status import status as st
from src.utils.response import ok, fail
from dal.shifts import ShiftsDAL
from common.errors import ErrorMessage as EM

_dal = ShiftsDAL()

def create_shift(event, _):
    sid = _dal.create(json.loads(event["body"]))
    return ok({"id": sid}, st.CREATED)

def list_shifts(event, _):
    qs = event.get("queryStringParameters") or {}
    return ok(_dal.list(status=qs.get("status")))

def get_shift(event, _):
    try:
        return ok(_dal.get(int(event["pathParameters"]["shift_id"])))
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)

def update_shift(event, _):
    try:
        _dal.update(int(event["pathParameters"]["shift_id"]), json.loads(event["body"]))
        return ok({"message": "updated"})
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)

def delete_shift(event, _):
    try:
        _dal.delete(int(event["pathParameters"]["shift_id"]))
        return ok({}, st.NO_CONTENT)
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)
