from flask import render_template
from podcastbuzz import app
from podcastbuzz.forms import LogonForm

# register home function
@app.route("/")
@app.route("/home")
def home():
    user = {'username': 'Ronan'}
    return render_template('home.html', user=user)

@app.route('/logon')
def logon():
    form=LogonForm()
    return render_template('logon.html', form=form)
