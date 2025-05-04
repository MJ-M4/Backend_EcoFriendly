from flask import Flask
from flask_cors import CORS
from Interface import auth, users, payments, shifts, vehicles, bins, hardware

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # register blueprints
    app.register_blueprint(auth.auth_bp,      url_prefix="/api/auth")
    app.register_blueprint(users.users_bp,    url_prefix="/api/users")
    app.register_blueprint(payments.payments_bp, url_prefix="/api/payments")
    app.register_blueprint(shifts.shifts_bp,  url_prefix="/api/shifts")
    app.register_blueprint(vehicles.vehicles_bp, url_prefix="/api/vehicles")
    app.register_blueprint(bins.bins_bp,      url_prefix="/api/bins")
    app.register_blueprint(hardware.hardware_bp, url_prefix="/api/hardware")

    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=5000)