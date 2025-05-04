import json
from common.status import status as st
from src.utils.response import ok, fail
from dal.bins import BinsDAL
from common.errors import ErrorMessage as EM

_dal = BinsDAL()

def create_bin(event, _):
    _dal.create(json.loads(event["body"]))
    return ok({"message": "created"}, st.CREATED)

def list_bins(_e, _):
    return ok(_dal.list())

def get_bin(event, _):
    try:
        return ok(_dal.get(event["pathParameters"]["bin_id"]))
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)

def update_bin(event, _):
    try:
        _dal.update(event["pathParameters"]["bin_id"], json.loads(event["body"]))
        return ok({"message": "updated"})
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)

def delete_bin(event, _):
    try:
        _dal.delete(event["pathParameters"]["bin_id"])
        return ok({}, st.NO_CONTENT)
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)
