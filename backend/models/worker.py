# backend/models/worker.py
from extensions import db  # Import db from extensions.py

class Worker(db.Model):
    __tablename__ = 'workers'
    id = db.Column(db.Integer, primary_key=True)
    identity = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    joining_date = db.Column(db.Date)
    worker_type = db.Column(db.Enum('Driver', 'Cleaner', 'Maintenance Worker'), nullable=False)