# Import the Flask module and create an instance of the Flask class
from flask import Flask
app = Flask(__name__)

# Set a secret key for the Flask application to enable session management and other features
app.secret_key = 'my_secret_key'

# Import other modules or blueprints that are part of this application
from . import connect, admin, member, moderator, utils
