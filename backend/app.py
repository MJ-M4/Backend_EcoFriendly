# backend/app.py
from flask import Flask
from flask_cors import CORS

# Import your Interface (blueprint) modules
from Interface.auth import auth_bp
from Interface.users import users_bp
from Interface.shifts import shifts_bp
from Interface.vehicles import vehicles_bp
from Interface.payments import payments_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Register blueprints under /api/ prefix
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(shifts_bp, url_prefix='/api/shifts')
app.register_blueprint(vehicles_bp, url_prefix='/api/vehicles')
app.register_blueprint(payments_bp, url_prefix='/api/payments')

if __name__ == '__main__':
    # run on port=5000; debug=True for dev
    app.run(debug=True, host='0.0.0.0', port=5000)
