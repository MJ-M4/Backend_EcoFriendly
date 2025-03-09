from flask import Flask
from flask_cors import CORS
from flask_backend.Config import Config
from flask_backend.model import db, hash_existing_passwords  # Correct import
from flask_backend.routes import auth_bp
from flask_backend.payments import payments_bp
from flask_backend.vehicles import vehicles_bp
from flask_backend.shifts import shifts_bp
from flask_backend.workers import workers_bp
from flask_backend.user import user_bp

app = Flask(__name__)
CORS(app)

# Load database config
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Register routes (Blueprint)
app.register_blueprint(auth_bp)
# workers.py
app.register_blueprint(workers_bp, url_prefix="/workers")
# shifts.py
app.register_blueprint(shifts_bp, url_prefix='/shifts')
# vehicles.py
app.register_blueprint(vehicles_bp, url_prefix='/vehicles')
# payments.py
app.register_blueprint(payments_bp, url_prefix='/payments')
# user.py
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        # Optionally hash any plaintext passwords
        hash_existing_passwords()

    # Start the Flask server
    app.run(debug=True)