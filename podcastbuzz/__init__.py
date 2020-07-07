from flask import Flask
from config import Config
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = "os.environ.get('SECRET_KEY')"
app.config['MONGO_DBNAME'] = "os.environ.get('MONGO_DBNAME')"
app.config['MONGO_URI'] = "os.environ.get('MONGO_URI')"
# app.config.from_object(Config)
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'logon'

# placing imports at the bottom to avoid circular dependancy issues
from podcastbuzz import routes
