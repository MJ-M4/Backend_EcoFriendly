# backend/routes/bins.py
from flask import Blueprint, request, jsonify
from extensions import db  # Import db from extensions.py
from models.bin import Bin
from models.user import User

bins_bp = Blueprint('bins', __name__)

@bins_bp.route('/', methods=['GET'])
def get_bins():
    bins = Bin.query.all()
    return jsonify([{
        'id': bin.id,
        'location': bin.location,
        'status': bin.status,
        'fill_level': bin.fill_level,
        'last_updated': bin.last_updated.isoformat(),
        'assigned_worker_id': bin.assigned_worker_id,
        'assigned_worker': bin.assigned_worker.username if bin.assigned_worker else None
    } for bin in bins]), 200

@bins_bp.route('/', methods=['POST'])
def add_bin():
    data = request.get_json()
    bin = Bin(
        id=data['id'],
        location=data['location'],
        status=data.get('status', 'Empty'),
        fill_level=data.get('fill_level', 0.0),
        assigned_worker_id=data.get('assigned_worker_id')
    )
    db.session.add(bin)
    db.session.commit()
    return jsonify({'message': 'Bin added successfully'}), 201

@bins_bp.route('/<id>', methods=['PUT'])
def update_bin(id):
    data = request.get_json()
    bin = Bin.query.get_or_404(id)
    bin.location = data.get('location', bin.location)
    bin.status = data.get('status', bin.status)
    bin.fill_level = data.get('fill_level', bin.fill_level)
    bin.assigned_worker_id = data.get('assigned_worker_id', bin.assigned_worker_id)
    db.session.commit()
    return jsonify({'message': 'Bin updated successfully'}), 200

@bins_bp.route('/<id>', methods=['DELETE'])
def delete_bin(id):
    bin = Bin.query.get_or_404(id)
    db.session.delete(bin)
    db.session.commit()
    return jsonify({'message': 'Bin deleted successfully'}), 200

# backend/routes/bins.py (add to the existing file)
@bins_bp.route('/alerts', methods=['GET'])
def get_alerts():
    bins = Bin.query.all()
    alerts = []
    for bin in bins:
        if bin.fill_level > 80:
            alerts.append({
                'id': bin.id + '_alert',
                'binId': bin.id,
                'type': 'Critical',
                'message': 'Bin is full',
                'time': bin.last_updated.strftime('%H:%M'),
                'date': bin.last_updated.strftime('%d-%m-%Y')
            })
        elif bin.fill_level > 50:
            alerts.append({
                'id': bin.id + '_alert',
                'binId': bin.id,
                'type': 'Warning',
                'message': 'Bin is near full',
                'time': bin.last_updated.strftime('%H:%M'),
                'date': bin.last_updated.strftime('%d-%m-%Y')
            })
    return jsonify(alerts), 200

# backend/routes/bins.py (add to the existing file)
@bins_bp.route('/reports', methods=['GET'])
def get_reports():
    bins = Bin.query.all()
    reports = [{
        'id': bin.id,
        'status': bin.status,
        'capacity': bin.fill_level,
        'location': bin.location,
        'lastCollected': bin.last_updated.strftime('%d-%m-%Y') if bin.last_updated else 'N/A'
    } for bin in bins]
    return jsonify(reports), 200