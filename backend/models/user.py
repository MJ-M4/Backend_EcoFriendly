# backend/models/user.py
from extensions import db  # Import db from extensions.py

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('worker', 'manager'), nullable=False)
    worker_type = db.Column(db.Enum('Driver', 'Cleaner', 'Maintenance Worker', 'Other'), default='Other')