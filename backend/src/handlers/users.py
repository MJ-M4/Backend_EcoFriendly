import json
from common.status import status as st
from src.utils.response import ok, fail
from dal.users import UsersDAL
from common.errors import ErrorMessage as EM

_dal = UsersDAL()

def create_user(event, _):
    try:
        _dal.create(json.loads(event["body"]))
        return ok({"message": "created"}, st.CREATED)
    except RuntimeError as exc:
        return fail(str(exc), st.CONFLICT)

def list_users(_e, _):
    return ok(_dal.list())

def get_user(event, _):
    try:
        return ok(_dal.get(event["pathParameters"]["user_id"]))
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)

def update_user(event, _):
    try:
        _dal.update(event["pathParameters"]["user_id"], json.loads(event["body"]))
        return ok({"message": "updated"})
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)

def delete_user(event, _):
    try:
        _dal.delete(event["pathParameters"]["user_id"])
        return ok({}, st.NO_CONTENT)
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)
