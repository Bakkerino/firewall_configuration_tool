from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dc7c6759cbb3d6ce0d57d790ec3b8ffb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=2) # sessietijd
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from configuratietool import routes