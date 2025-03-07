# backend/app.py
from flask import Flask
from flask_cors import CORS
from extensions import db  # Import db from extensions.py

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Jayusi2024@localhost/urban_waste_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with the app
db.init_app(app)

# Import and register blueprints
from routes.auth import auth_bp
from routes.bins import bins_bp
from routes.workers import workers_bp
from routes.shifts import shifts_bp
from routes.payments import payments_bp
from routes.vehicles import vehicles_bp
from routes.settings import settings_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(bins_bp, url_prefix='/api/bins')
app.register_blueprint(workers_bp, url_prefix='/api/workers')
app.register_blueprint(shifts_bp, url_prefix='/api/shifts')
app.register_blueprint(payments_bp, url_prefix='/api/payments')
app.register_blueprint(vehicles_bp, url_prefix='/api/vehicles')
app.register_blueprint(settings_bp, url_prefix='/api/settings')

if __name__ == '__main__':
    app.run(debug=True, port=5000)