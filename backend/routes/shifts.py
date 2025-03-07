# backend/routes/shifts.py
from flask import Blueprint, request, jsonify
from extensions import db  # Import db from extensions.py
from models.shift import Shift

shifts_bp = Blueprint('shifts', __name__)

@shifts_bp.route('/', methods=['GET'])
def get_shifts():
    shifts = Shift.query.all()
    return jsonify([{
        'id': shift.id,
        'worker_id': shift.worker_id,
        'worker_name': shift.worker.name,
        'date': shift.date.isoformat(),
        'start_time': shift.start_time.strftime('%H:%M:%S'),
        'end_time': shift.end_time.strftime('%H:%M:%S'),
        'location': shift.location
    } for shift in shifts]), 200

@shifts_bp.route('/', methods=['POST'])
def add_shift():
    data = request.get_json()
    shift = Shift(
        worker_id=data['worker_id'],
        date=data['date'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        location=data['location']
    )
    db.session.add(shift)
    db.session.commit()
    return jsonify({'message': 'Shift added successfully'}), 201

@shifts_bp.route('/<int:id>', methods=['DELETE'])
def delete_shift(id):
    shift = Shift.query.get_or_404(id)
    db.session.delete(shift)
    db.session.commit()
    return jsonify({'message': 'Shift deleted successfully'}), 200