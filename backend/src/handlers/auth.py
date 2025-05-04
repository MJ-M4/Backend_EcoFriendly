import json
from common.status import status as st
from common.errors import ErrorMessage as EM
from src.utils.response import ok, fail
from dal.users import UsersDAL

_udl = UsersDAL()

def login(event, _ctx):
    data = json.loads(event["body"] or "{}")
    uid  = data.get("user_id")
    pw   = data.get("password")
    try:
        user = _udl.verify(uid, pw)
        return ok(user)
    except RuntimeError as exc:
        msg = str(exc)
        code = st.UNAUTHORIZED if msg == EM.INVALID_CREDENTIALS else st.NOT_FOUND
        return fail(msg, code)
