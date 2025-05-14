from flask import Flask
from flask_cors import CORS

from src.errors.handlers import register_error_handlers
from src.interface import register_blueprints

def create_app() -> Flask:
    """Flask factory – registers CORS, errors and route blueprints."""
    app = Flask(__name__)
    CORS(app)
    register_error_handlers(app)
    register_blueprints(app)
    return app

# WSGI entry-point for serverless-wsgi
flask_app = create_app()