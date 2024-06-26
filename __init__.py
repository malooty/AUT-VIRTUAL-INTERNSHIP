from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for cross-origin requests

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
