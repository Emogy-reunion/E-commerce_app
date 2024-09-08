'''
This module initializes the flask instance
Initializes the configuration settings
'''
from flask import Flask
from create_app import create_app
from model import Users, db, bcrypt
from routes.authentication import auth
from routes.verification import verify
from routes.reset import reset
from routes.dashboard import dash
from routes.uploads import post
from utils.verification import mail
from flask_login import LoginManager


# create the app instance
app = create_app()

db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)
loginmanager = LoginManager(app)
loginmanager.login_view = 'login'

# register blueprints
app.register_blueprint(auth)
app.register_blueprint(verify)
app.register_blueprint(reset)
app.register_blueprint(dash)
app.register_blueprint(post)

@loginmanager.user_loader
def load_user(user_id):
    return db.session.get(Users, int(user_id))

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
