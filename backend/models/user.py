from DataLayer.db import db
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('worker', 'manager'), nullable=False)
    worker_type = db.Column(db.Enum('Driver', 'Cleaner', 'Maintenance Worker', 'Other'), default='Other')

    def set_password(self, password):
        self.password = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'worker_type': self.worker_type
        }

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def create(cls, username, role, password, worker_type='Other'):
        user = cls(username=username, role=role, worker_type=worker_type)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user