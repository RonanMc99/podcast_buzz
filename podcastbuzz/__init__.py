from flask import Flask
from config import Config
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object(Config)
mongo = PyMongo(app)

# placing imports at the bottom to avoid circular dependancy issues
from podcastbuzz import routes
