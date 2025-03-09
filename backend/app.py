# app.py
from flask import Flask
from flask_cors import CORS
from flask_backend.Config import Config
from flask_backend.model import db, hash_existing_passwords
from flask_backend.routes import auth_bp

app = Flask(__name__)
CORS(app)

# Load database config
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Register routes (Blueprint)
app.register_blueprint(auth_bp)
from flask_backend.workers import workers_bp
app.register_blueprint(workers_bp, url_prefix="/workers")


if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        # Optionally hash any plaintext passwords
        hash_existing_passwords()

    # Start the Flask server
    app.run(debug=True)
