from flask import render_template, redirect, url_for,
from podcastbuzz import app, mongo
from podcastbuzz.forms import LogonForm, SignupForm

# register home function
@app.route("/")
@app.route("/home")
def home():
    user = {'username': 'Ronan'}
    return render_template('home.html', user=user)

# @app.route('/logon')
# def logon():
#     form=LogonForm()
#     return render_template('logon.html', form=form)

# Create the 'register' view
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check to see if user is already logged in, if so, can't log in again
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    forms=SignupForm()
    # when the form is submitted...
    if forms.validate_on_submit():
        # create an instance of MongoDB and get all users
        users = mongo.db.users
