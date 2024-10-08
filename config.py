import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    """
    Stores the application configuration settings
    """
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # WTF_CSRF_ENABLED = False
    MAIL_USERNAME = os.getenv('EMAIL')
    MAIL_PASSWORD = os.getenv('PASSWORD')
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # set max upload size to 16mb

    @staticmethod
    def ensure_upload_folder():
        """
        Ensure the upload folder exists. If not, create it.
        """
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
