import json, datetime
from common.status import status

def _enc(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError

def ok(body, st=status.OK):
    return {
        "statusCode": st.value,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, default=_enc),
    }

def fail(msg: str, st):
    return ok({"message": msg}, st)
