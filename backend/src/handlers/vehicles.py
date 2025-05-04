import json
from common.status import status as st
from src.utils.response import ok, fail
from dal.vehicles import VehiclesDAL
from common.errors import ErrorMessage as EM

_dal = VehiclesDAL()

def create_vehicle(event, _):
    _dal.create(json.loads(event["body"]))
    return ok({"message": "created"}, st.CREATED)

def list_vehicles(_e, _):
    return ok(_dal.list())

def get_vehicle(event, _):
    try:
        return ok(_dal.get(int(event["pathParameters"]["vehicle_id"])))
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)

def update_vehicle(event, _):
    try:
        _dal.update(int(event["pathParameters"]["vehicle_id"]), json.loads(event["body"]))
        return ok({"message": "updated"})
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)

def delete_vehicle(event, _):
    try:
        _dal.delete(int(event["pathParameters"]["vehicle_id"]))
        return ok({}, st.NO_CONTENT)
    except RuntimeError as exc:
        return fail(str(exc), st.NOT_FOUND)
