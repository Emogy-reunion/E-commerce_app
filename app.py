'''
This module initializes the flask instance
Initializes the configuration settings
'''
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


# create the app instance
app = Flask(__name__)

# initialize app with configuration settings
app.config.from_object(Config)

# create the db instance
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=True)
