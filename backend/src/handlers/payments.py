import json
from common.status import status as st
from src.utils.response import ok, fail
from dal.payments import PaymentsDAL
from common.errors import ErrorMessage as EM

_dal = PaymentsDAL()

def create_payment(event, _):
    _dal.create(json.loads(event["body"]))
    return ok({"message": "created"}, st.CREATED)

def list_payments(_e, _):
    return ok(_dal.list())

def get_payment(event, _):
    try:
        return ok(_dal.get(int(event["pathParameters"]["payment_id"])))
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)

def mark_paid(event, _):
    pid = int(event["pathParameters"]["payment_id"])
    date_str = (event.get("queryStringParameters") or {}).get("date")
    try:
        _dal.set_paid(pid, date_str)
        return ok({"message": "paid"})
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)

def delete_payment(event, _):
    try:
        _dal.delete(int(event["pathParameters"]["payment_id"]))
        return ok({}, st.NO_CONTENT)
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)
