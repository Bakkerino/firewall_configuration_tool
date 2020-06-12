from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["ALLOWED_IMPORTFILE_EXTENSIONS"] = ["CONF", "TXT"]
app.config["MAX_FILESIZE"] = 0.095367431640625 * 1024 * 1024 *10 # 1000kB
app.config["CFG_UPLOADS"] = "./cvf/file_cache/"
app.config['SECRET_KEY'] = 'dc7c6759cbb3d6ce0d57d790ec3b8ffb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginmanager = LoginManager(app)
loginmanager.login_view = 'login'
loginmanager.login_message_category = 'info'
loginmanager.login_message = u"Log alstublieft in om toegang te krijgen tot deze pagina."

from cvf import routes





