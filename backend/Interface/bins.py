from flask import Blueprint, request, jsonify, make_response
from Models.Bin import Bin
from pydantic import BaseModel, ValidationError
from http import HTTPStatus

bins_bp = Blueprint('bins', __name__)

class BinModel(BaseModel):
    id: str
    location: str
    status: str = "Empty"
    fill_level: float = 0.0
    assigned_worker_id: int = None

@bins_bp.route('/', methods=['GET'])
def get_bins():
    bins = Bin.get_all()
    return make_response(jsonify([b.to_dict() for b in bins]), HTTPStatus.OK)

@bins_bp.route('/', methods=['POST'])
def add_bin():
    try:
        data = BinModel(**request.get_json())
    except ValidationError as e:
        return make_response(jsonify({'error': e.errors()}), HTTPStatus.BAD_REQUEST)
    
    new_bin = Bin.create(
        id=data.id,
        location=data.location,
        status=data.status,
        fill_level=data.fill_level,
        assigned_worker_id=data.assigned_worker_id
    )
    return make_response(jsonify(new_bin.to_dict()), HTTPStatus.CREATED)

@bins_bp.route('/<bin_id>', methods=['PUT'])
def update_bin(bin_id):
    bin_obj = Bin.get_by_id(bin_id)
    if not bin_obj:
        return make_response(jsonify({'error': 'Bin not found'}), HTTPStatus.NOT_FOUND)
    
    req_data = request.get_json()
    bin_obj.update(
        location=req_data.get('location'),
        status=req_data.get('status'),
        fill_level=req_data.get('fill_level'),
        assigned_worker_id=req_data.get('assigned_worker_id')
    )
    return make_response(jsonify(bin_obj.to_dict()), HTTPStatus.OK)

@bins_bp.route('/<bin_id>', methods=['DELETE'])
def delete_bin(bin_id):
    bin_obj = Bin.get_by_id(bin_id)
    if not bin_obj:
        return make_response(jsonify({'error': 'Bin not found'}), HTTPStatus.NOT_FOUND)
    
    bin_obj.delete()
    return make_response(jsonify({'message': 'Bin deleted successfully'}), HTTPStatus.OK)