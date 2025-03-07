# backend/routes/settings.py
from flask import Blueprint, request, jsonify
from extensions import db  # Import db from extensions.py
from models.user_settings import UserSettings
from models.user import User

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/<int:user_id>', methods=['GET'])
def get_settings(user_id):
    settings = UserSettings.query.filter_by(user_id=user_id).first_or_404()
    return jsonify({
        'id': settings.id,
        'name': settings.name,
        'language': settings.language,
        'theme': settings.theme,
        'notifications': {
            'alerts': settings.alerts_notifications,
            'reports': settings.reports_notifications,
            'shifts': settings.shifts_notifications
        }
    }), 200

@settings_bp.route('/<int:user_id>', methods=['PUT'])
def update_settings(user_id):
    data = request.get_json()
    settings = UserSettings.query.filter_by(user_id=user_id).first_or_404()
    settings.name = data.get('name', settings.name)
    settings.language = data.get('language', settings.language)
    settings.theme = data.get('theme', settings.theme)
    settings.alerts_notifications = data.get('notifications', {}).get('alerts', settings.alerts_notifications)
    settings.reports_notifications = data.get('notifications', {}).get('reports', settings.reports_notifications)
    settings.shifts_notifications = data.get('notifications', {}).get('shifts', settings.shifts_notifications)
    db.session.commit()
    return jsonify({'message': 'Settings updated successfully'}), 200