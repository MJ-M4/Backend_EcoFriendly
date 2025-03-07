# backend/models/vehicle.py
from extensions import db  # Import db from extensions.py

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    license_plate = db.Column(db.String(10), unique=True, nullable=False)
    status = db.Column(db.Enum('Available', 'In Use', 'Under Maintenance'), default='Available')
    last_maintenance = db.Column(db.Date)