# backend/routes/workers.py
from flask import Blueprint, request, jsonify
from extensions import db  # Import db from extensions.py
from models.worker import Worker

workers_bp = Blueprint('workers', __name__)

@workers_bp.route('/', methods=['GET'])
def get_workers():
    workers = Worker.query.all()
    return jsonify([{
        'id': worker.id,
        'identity': worker.identity,
        'name': worker.name,
        'phone': worker.phone,
        'location': worker.location,
        'joining_date': worker.joining_date.isoformat() if worker.joining_date else None,
        'worker_type': worker.worker_type
    } for worker in workers]), 200

@workers_bp.route('/', methods=['POST'])
def add_worker():
    data = request.get_json()
    worker = Worker(
        identity=data['identity'],
        name=data['name'],
        phone=data['phone'],
        location=data['location'],
        joining_date=data['joining_date'],
        worker_type=data['worker_type']
    )
    db.session.add(worker)
    db.session.commit()
    return jsonify({'message': 'Worker added successfully'}), 201

@workers_bp.route('/<int:id>', methods=['DELETE'])
def delete_worker(id):
    worker = Worker.query.get_or_404(id)
    db.session.delete(worker)
    db.session.commit()
    return jsonify({'message': 'Worker deleted successfully'}), 200