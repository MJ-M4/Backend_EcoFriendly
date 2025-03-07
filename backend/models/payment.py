# backend/models/payment.py
from extensions import db  # Import db from extensions.py

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.Date)
    status = db.Column(db.Enum('Paid', 'Pending'), nullable=False)
    notes = db.Column(db.Text)
    worker = db.relationship('Worker', backref='payments')