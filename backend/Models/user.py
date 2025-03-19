# backend/Models/user.py
from Models.base_model import BaseModel
import bcrypt
from DataLayer.database import Database
from DataLayer.errors import DB_INVALID_CREDENTIALS

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
        self.db = Database()

    def load_by_id(self, user_id):
        self.db.connect()
        try:
            user_data = self.db.fetch_user_by_id(user_id)
            self.id = user_data['id']
            self.user_id = user_data['user_id']
            self.password = user_data['password']
            self.role = user_data['role']
            self.name = user_data['name']
            self.phone = user_data['phone']
            self.location = user_data['location']
            self.joining_date = user_data['joining_date']
            self.worker_type = user_data['worker_type']
        finally:
            self.db.disconnect()

    def verify_password(self, plain_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.password.encode('utf-8'))

    def login(self, user_id, password):
        self.load_by_id(user_id)
        if not self.verify_password(password):
            raise Exception(DB_INVALID_CREDENTIALS)
        return self

    def add_user(self, user_data):
        plain_password = user_data['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(plain_password, bcrypt.gensalt()).decode('utf-8')
        user_data['password'] = hashed_password

        self.db.connect()
        try:
            self.db.insert_user(user_data)
            self.user_id = user_data['user_id']
            self.password = hashed_password
            self.role = user_data['role']
            self.name = user_data['name']
            self.phone = user_data['phone']
            self.location = user_data['location']
            self.joining_date = user_data['joining_date']
            self.worker_type = user_data['worker_type']
            return self
        finally:
            self.db.disconnect()

    def get_all_users(self):
        self.db.connect()
        try:
            return self.db.fetch_all_users()
        finally:
            self.db.disconnect()

    def delete_user(self, user_id):
        self.db.connect()
        try:
            self.db.delete_user(user_id)
        finally:
            self.db.disconnect()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'password': self.password,  # Include the hashed password
            'role': self.role,
            'name': self.name,
            'phone': self.phone,
            'location': self.location,
            'joining_date': str(self.joining_date) if self.joining_date else None,
            'worker_type': self.worker_type
        }