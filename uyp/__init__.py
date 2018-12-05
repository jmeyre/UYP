from flask import Flask
from flask_bcrypt import Bcrypt

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

# The name of the database
DB_NAME = 'ufyp'

bcrypt = Bcrypt(app)

from uyp import routes
