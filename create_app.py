"""
App factory
Creates app so that it can be imported by 
    other modules without causing circular imports
"""
from flask import Flask
from config import Config


def create_app():
    """
    Creates the app instance
    Initializes it with configuration settings
    returns the app instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    return app
