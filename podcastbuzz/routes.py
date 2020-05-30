from podcastbuzz import app
from flask import render_template

# register home function
@app.route("/")
@app.route("/home")
def home():
    return "<h1>Welcome to PodcastBuzz</h1>"