from flask import Flask
from flask_cors import CORS
from DataLayer.db import db, init_db
from Interface.auth import auth_bp
from Interface.bins import bins_bp
from Interface.payments import payments_bp
from Interface.shifts import shifts_bp
from Interface.vehicles import vehicles_bp
from Interface.workers import workers_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # Enable CORS for all routes

# Initialize extensions
init_db(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(bins_bp, url_prefix='/api/bins')
app.register_blueprint(payments_bp, url_prefix='/api/payments')
app.register_blueprint(shifts_bp, url_prefix='/api/shifts')
app.register_blueprint(vehicles_bp, url_prefix='/api/vehicles')
app.register_blueprint(workers_bp, url_prefix='/api/workers')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)