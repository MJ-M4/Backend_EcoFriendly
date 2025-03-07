# backend/models/user_settings.py
from extensions import db  # Import db from extensions.py

class UserSettings(db.Model):
    __tablename__ = 'user_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(50), default='English')
    theme = db.Column(db.String(50), default='Light')
    alerts_notifications = db.Column(db.Boolean, default=True)
    reports_notifications = db.Column(db.Boolean, default=True)
    shifts_notifications = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref='settings')