# __init__.py
from flask import Flask
from flask_cors import CORS
from flask_backend.Config import Config
from flask_backend.model import db
from flask_backend.routes import auth_bp
from flask_backend.workers import workers_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(workers_bp, url_prefix="/workers")

    with app.app_context():
        db.create_all()

    return app