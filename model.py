from datetime import datetime, timezone
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
    registered_on = db.Column(db.DateTime, default=datetime.now(timezone.utc)
    role = db.Column(db.String(50), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    sneakers = db.relationship('Sneakers', lazy=True, backref='user', cascade='all, delete-orphan')
    cart = db.relationship('Cart', uselist=False, lazy=True, backref='user', cascade='all, delete-orphan')

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

class Sneakers(db.Model):
    '''
    stores the sneaker's collection
    one user can have multiple uploads
    '''
    __tablename__ = 'sneakers'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    images = db.relationship('Images', backref='sneaker', cascade='all, delete-orphan')

    def __init__(self, name, price, description, user_id, brand, gender):
        '''
        initializes the table with data
        '''
        self.name = name
        self.price = price
        self.description = description
        self.user_id = user_id
        self.brand = brand
        self.gender = gender

class Images(db.Model):
    '''
    stores the sneaker's images
    one sneaker can have multiple images
    '''
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.String(350), nullable=False)
    sneaker_id = db.Column(db.Integer, db.ForeignKey('sneakers.id'), nullable=False)

    def __init__(self, filename, sneaker_id):
        '''
        initializes the table with data
        '''
        self.filename = filename
        self.sneaker_id = sneaker_id

class Cart(db.Model):
    '''
    stores items a user wants to purchase before checkout
    '''
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', unique=True), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    items = db.relationship('CartItems', lazy=True, backref='cart', cascade='all, delete_orphan')

class CartItems(db.Model):
    '''
    stores the items a user adds to cart
    '''
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)  # Foreign key to the Product table
    product_name = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

