from flask import Blueprint, request, jsonify, make_response
from Models.Worker import Worker
from pydantic import BaseModel, ValidationError
from http import HTTPStatus

workers_bp = Blueprint('workers', __name__)

class WorkerModel(BaseModel):
    identity: str
    name: str
    phone: str
    location: str
    joining_date: str
    worker_type: str

@workers_bp.route('/', methods=['GET'])
def get_workers():
    workers = Worker.get_all()
    return make_response(jsonify([w.to_dict() for w in workers]), HTTPStatus.OK)

@workers_bp.route('/', methods=['POST'])
def add_worker():
    try:
        data = WorkerModel(**request.get_json())
    except ValidationError as e:
        return make_response(jsonify({'error': e.errors()}), HTTPStatus.BAD_REQUEST)
    
    worker = Worker.create(
        identity=data.identity,
        name=data.name,
        phone=data.phone,
        location=data.location,
        joining_date=data.joining_date,
        worker_type=data.worker_type
    )
    return make_response(jsonify(worker.to_dict()), HTTPStatus.CREATED)

@workers_bp.route('/<int:worker_id>', methods=['PUT'])
def update_worker(worker_id):
    worker = Worker.get_by_id(worker_id)
    if not worker:
        return make_response(jsonify({'error': 'Worker not found'}), HTTPStatus.NOT_FOUND)
    
    req_data = request.get_json()
    worker.update(
        identity=req_data.get('identity'),
        name=req_data.get('name'),
        phone=req_data.get('phone'),
        location=req_data.get('location'),
        joining_date=req_data.get('joining_date'),
        worker_type=req_data.get('worker_type')
    )
    return make_response(jsonify(worker.to_dict()), HTTPStatus.OK)

@workers_bp.route('/<int:worker_id>', methods=['DELETE'])
def delete_worker(worker_id):
    worker = Worker.get_by_id(worker_id)
    if not worker:
        return make_response(jsonify({'error': 'Worker not found'}), HTTPStatus.NOT_FOUND)
    
    worker.delete()
    return make_response(jsonify({'message': 'Worker deleted successfully'}), HTTPStatus.OK)