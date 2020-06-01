from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# placing imports at the bottom to avoid circular dependancy issues
from podcastbuzz import routes