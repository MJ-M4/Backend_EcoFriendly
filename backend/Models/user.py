# backend/Models/user.py
import bcrypt
from Models.base_model import BaseModel
from DataLayer.errors import (
    DB_INVALID_CREDENTIALS,
    DB_USER_NOT_FOUND,
    DB_USER_ALREADY_EXISTS
)
from DataLayer.users_datalayer import UsersDataLayer

class User(BaseModel):
    def __init__(self):
        super().__init__()
        self.user_id = None
        self.password = None
        self.role = None
        self.name = None
        self.phone = None
        self.location = None
        self.joining_date = None
        self.worker_type = None
        self.dl = UsersDataLayer()

    def load_by_id(self, user_id):
        data = self.dl.fetch_user_by_id(user_id)
        self._fill_data(data)

    def _fill_data(self, data):
        # Fill model attributes from DB dict
        # self.id (the numeric autoincrement?) if your DB has `id` column:
        self.id = data.get('id', None)
        self.user_id = data['user_id']
        self.password = data['password']
        self.role = data['role']
        self.name = data['name']
        self.phone = data['phone']
        self.location = data['location']
        self.joining_date = data['joining_date']
        self.worker_type = data['worker_type']

    def verify_password(self, plain_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.password.encode('utf-8'))

    def login(self, user_id, password):
        self.load_by_id(user_id)
        if not self.verify_password(password):
            raise Exception(DB_INVALID_CREDENTIALS)
        return self

    def add_user(self, user_data):
        """Check if user already exists, then hash password, then insert."""
        # Check existence
        try:
            existing = self.dl.fetch_user_by_id(user_data['user_id'])
            if existing:
                # If it didn't raise DB_USER_NOT_FOUND, user must exist
                raise Exception(DB_USER_ALREADY_EXISTS)
        except Exception as e:
            if str(e) != DB_USER_NOT_FOUND:
                # Some other error
                raise

        # Hash the password
        plain_pw = user_data['password'].encode('utf-8')
        hashed_pw = bcrypt.hashpw(plain_pw, bcrypt.gensalt()).decode('utf-8')
        user_data['password'] = hashed_pw

        self.dl.insert_user(user_data)
        # Load the inserted user so we have all fields
        data = self.dl.fetch_user_by_id(user_data['user_id'])
        self._fill_data(data)
        return self

    def get_all_users(self):
        return self.dl.fetch_all_users()

    def delete_user(self, user_id):
        self.dl.delete_user(user_id)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'password': self.password,  # ideally not returned in production
            'role': self.role,
            'name': self.name,
            'phone': self.phone,
            'location': self.location,
            'joining_date': self.joining_date,
            'worker_type': self.worker_type
        }
