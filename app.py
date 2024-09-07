'''
This module initializes the flask instance
Initializes the configuration settings
'''
from flask import Flask


# create the app instance
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)
