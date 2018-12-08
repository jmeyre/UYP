from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '2d7596cbe025473acb2bb5d8f268f5a5'

# The parameters for connecting to the database
config = {
    'user': 'admin',
    'password': 'admin',
    'host': 'localhost',
    'database': 'ufyp',
    'raise_on_warnings': True
}

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from uyp import routes
