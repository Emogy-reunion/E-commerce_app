"""
Persists the model to the database
"""
from app import app, db
from model import Users

def create_model():
    """
    creates the models in the database
    creates the initial admin
    """
    with app.app_context():
        db.create_all()
        if Users.query.filter_by(email='mv7786986@gmail.com').first() is None:
            try:
                admin = Users(firstname='Mark', lastname='Mugendi',
                            email='mv7786986@gmail.com', password='&Admin23', role='admin')
                db.session.add(admin)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
