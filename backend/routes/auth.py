# backend/routes/auth.py
from flask import Blueprint, request, jsonify
from extensions import db  # Import db from extensions.py
from models.user import User
import smtplib
from email.mime.text import MIMEText


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    print(f"Received login request: username={username}, password={password}")  # Debug log

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'worker_type': user.worker_type
    }), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = User.query.filter_by(username=email).first()  # Assuming username is email for simplicity
    if not user:
        return jsonify({'error': 'No user found with that email'}), 404

    # Simulate sending reset email (replace with real SMTP configuration)
    try:
        msg = MIMEText(f'Click this link to reset your password: http://localhost:3000/reset-password/{user.id}')
        msg['Subject'] = 'Password Reset Request'
        msg['From'] = 'your-email@example.com'
        msg['To'] = email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('your-email@example.com', 'your-app-password')  # Use App Password for Gmail
            server.send_message(msg)

        return jsonify({'message': 'Password reset link sent to your email'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500