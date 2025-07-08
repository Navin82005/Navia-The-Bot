import os
import json
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from .routes import routes  # chat route
from .helper import CONFIG  # load config globally for use across modules

def create_app():
    load_dotenv()

    app = Flask(__name__)

    cors_origins = CONFIG.get("cors_origins", ["*"])
    CORS(app, resources={r"/*": {"origins": cors_origins}})

    app.register_blueprint(routes)

    return app
