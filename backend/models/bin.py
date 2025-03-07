# backend/models/bin.py
from extensions import db  # Import db from extensions.py

class Bin(db.Model):
    __tablename__ = 'bins'
    id = db.Column(db.String(50), primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Enum('Full', 'Empty', 'Near Full'), default='Empty')
    fill_level = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp())
    assigned_worker_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assigned_worker = db.relationship('User', backref='bins')