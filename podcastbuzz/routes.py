from podcastbuzz import app
from flask import render_template

# register home function
@app.route("/")
@app.route("/home")
def home():
    return render_template('base.html')