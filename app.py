'''
This module initializes the flask instance
Initializes the configuration settings
'''
from flask import Flask
from create_app import create_app
from model import Users, db, bcrypt


# create the app instance
app = create_app()

db.init_app(app)
bcrypt.init_app(app)

def create_models():
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
create_models()


if __name__ == "__main__":
    app.run(debug=True)
