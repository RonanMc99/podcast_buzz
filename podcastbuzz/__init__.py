from flask import Flask

app = Flask(__name__)

# placing imports at the bottom to avoid circular dependancy issues
from app import routes
