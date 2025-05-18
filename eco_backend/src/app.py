# src/app.py
from flask import Flask
from src.interface.auth_routes import auth_bp
from src.interface.employee_routes import employee_bp


app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)