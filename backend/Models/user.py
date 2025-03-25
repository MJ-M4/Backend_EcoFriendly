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
        self.password = None  # Hashed password
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
        self.id = data.get('id')
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
        try:
            self.dl.fetch_user_by_id(user_data['user_id'])
            raise Exception(DB_USER_ALREADY_EXISTS)
        except Exception as e:
            if str(e) != DB_USER_NOT_FOUND:
                raise
        plain_pw = user_data['password'].encode('utf-8')
        hashed_pw = bcrypt.hashpw(plain_pw, bcrypt.gensalt()).decode('utf-8')
        user_data['password'] = hashed_pw
        self.dl.insert_user(user_data)
        data = self.dl.fetch_user_by_id(user_data['user_id'])
        self._fill_data(data)
        return self

    def get_all_users(self):
        return self.dl.fetch_all_users()

    def delete_user(self, user_id):
        self.dl.delete_user(user_id)

    def update_password(self, user_id, old_password, new_password):
        self.load_by_id(user_id)
        if not self.verify_password(old_password):
            raise Exception(DB_INVALID_CREDENTIALS)
        hashed_new = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.dl.update_user_password(user_id, hashed_new)
        self.password = hashed_new
        return True

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role': self.role,
            'name': self.name,
            'phone': self.phone,
            'location': self.location,
            'joining_date': self.joining_date,
            'worker_type': self.worker_type
        }
