from datetime import datetime
from app import db


class Users(db.Model):
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
    roles = db.Column(db.String(50), default='guest')
    verified = db.Column(db.Boolean, default=False)

    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password)
