# src/app.py
from flask import Flask
from src.interface.auth_routes import auth_bp
from src.interface.employee_routes import employee_bp
from src.interface.vehicle_routes import vehicle_bp
from src.interface.bin_routes import bin_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(vehicle_bp)
app.register_blueprint(bin_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
