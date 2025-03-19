# backend/app.py
from flask import Flask
from flask_cors import CORS
from Interface.auth import auth_bp
from Interface.users import users_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Explicitly allow localhost:3000

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(users_bp, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)