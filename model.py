from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from flask_login import UserMixin
from create_app import create_app

app = create_app()
db = SQLAlchemy()
bcrypt = Bcrypt()

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

class Users(UserMixin, db.Model):
    """
    A representation of users table
    Each attribute corresponds to a column in the table
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(50), nullable=False)
    verified = db.Column(db.Boolean, default=False)

    def __init__(self, firstname, lastname, email, password, role='guest'):
        self.first_name = firstname
        self.last_name = lastname
        self.email = email
        self.role = role
        self.set_password(password)

    def set_password(self, password):
        """
        Hashes and stores the password
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """
        compares the user password and stored hash
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_token(self):
        """
        serializes the user id as a token and used for verification
        """
        return serializer.dumps({'user_id': self.id})

    @staticmethod
    def verify_token(token):
        '''
        deserializes the token and verifies the user if the token is valid
        '''
        try:
            data = serializer.loads(token, max_age=3600)
            return db.session.query(Users, data['user_id'])
        except Exception as e:
            return None

