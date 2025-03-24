# backend/Models/shift.py
from Models.base_model import BaseModel
from DataLayer.errors import DB_USER_NOT_FOUND
from DataLayer.shifts_datalayer import ShiftsDataLayer
from DataLayer.users_datalayer import UsersDataLayer

class Shift(BaseModel):
    def __init__(self):
        super().__init__()
        self.worker_id = None
        self.worker_name = None
        self.worker_type = None
        self.phone = None
        self.location = None
        self.date = None
        self.start_time = None
        self.end_time = None
        self.status = None
        self.submitted_at = None

        self.shiftsDL = ShiftsDataLayer()
        self.usersDL = UsersDataLayer()

    def create_shift(self, shift_data):
        # 1) Ensure user_id exists & is a worker
        user = self.usersDL.fetch_user_by_id(shift_data['worker_id'])  # may raise DB_USER_NOT_FOUND
        if user['role'] != 'worker':
            raise Exception("Only workers can be assigned shifts")

        # 2) Insert shift
        # Fill worker_name/type from user
        shift_data['worker_name'] = user['name']
        shift_data['worker_type'] = user['worker_type']

        shift_id = self.shiftsDL.insert_shift(shift_data)
        self.id = shift_id
        self.worker_id = shift_data['worker_id']
        self.worker_name = shift_data['worker_name']
        self.worker_type = shift_data['worker_type']
        self.phone = user['phone']
        self.location = shift_data['location']
        self.date = shift_data['date']
        self.start_time = shift_data['start_time']
        self.end_time = shift_data['end_time']
        self.status = shift_data['status']
        return self

    def get_shifts_by_worker(self, worker_id, status=None):
        shifts = self.shiftsDL.fetch_shifts_by_worker(worker_id, status)
        # Optionally fill phone
        for s in shifts:
            user_data = self.usersDL.fetch_user_by_id(s['worker_id'])
            s['phone'] = user_data['phone']
        return shifts

    def get_all_shifts(self, status=None):
        shifts = self.shiftsDL.fetch_all_shifts(status)
        for s in shifts:
            user_data = self.usersDL.fetch_user_by_id(s['worker_id'])
            s['phone'] = user_data['phone']
        return shifts

    def approve_shift(self, shift_id):
        self.shiftsDL.update_shift_status(shift_id, 'approved')

    def deny_shift(self, shift_id):
        self.shiftsDL.update_shift_status(shift_id, 'denied')

    def delete_shift(self, shift_id):
        self.shiftsDL.delete_shift(shift_id)

    def to_dict(self):
        return {
            'id': self.id,
            'worker_id': self.worker_id,
            'worker_name': self.worker_name,
            'worker_type': self.worker_type,
            'phone': self.phone,
            'location': self.location,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'status': self.status,
            'submitted_at': self.submitted_at
        }
