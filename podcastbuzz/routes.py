from flask import render_template, redirect, url_for, request, flash, Response
from flask_login import current_user, login_user, logout_user, login_required
from podcastbuzz import app, mongo, bcrypt
from podcastbuzz.forms import LogonForm, SignupForm
from podcastbuzz.models import User
from podcastbuzz.listen_notes import search_podcast
from bson.objectid import ObjectId
import json


# register home function
@app.route("/")
@app.route("/home")
def home():
    user = {'username': 'Ronan'}
    return render_template('home.html', user=user)


# Create the 'register' view
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check to see if user is already logged in, if so, can't log in again
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    forms = SignupForm()
    # when the form is submitted...
    if forms.validate_on_submit():
        # create an instance of MongoDB and get all users
        users = mongo.db.users
        # see if the (unique) email already exists
        existing_user = users.find_one({'email': request.form['email']})
        # if the user doesn't exist, hash the password and store the user in DB
        if existing_user is None:
            hash_pass = bcrypt.generate_password_hash(
                forms.password.data).decode('utf-8')
            users.insert_one({
                            'username': request.form['username'],
                            'password': hash_pass,
                            'email': request.form['email']})
            flash('Your account has been created. Please logon', 'success')
            return redirect(url_for('logon'))
        flash('Sorry that email is already taken. Please choose another')
    return render_template('register.html', forms=forms, title='Sign Up')


# Create the 'logon' view
@app.route('/logon', methods=['GET', 'POST'])
def logon():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    forms = LogonForm()
    if forms.validate_on_submit():
        users = mongo.db.users
        # try to find one with same name
        db_user = users.find_one({'email': request.form['email']})
        # authenticate user
        if db_user and bcrypt.check_password_hash(db_user['password'], request.form['password']):
            loginuser = User(db_user)
            login_user(loginuser, remember=forms.remember.data)
            nextpage = request.args.get('next')
            return redirect(nextpage) if nextpage else redirect(url_for('home'))
        else:
            flash('Login unsuccessful! Please try again', 'danger')
    return render_template('logon.html', forms=forms, title='Logon')


# Create the 'logout' view
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# search API
@app.route('/search', methods=['GET'])
def search():
    query_param = request.args.get('q')
    response = search_podcast(query_param)
    modified_object = []
    for result in response['results']:
        modified_object.append(
            {
                'podcast_title_original': result['podcast_title_original'],
                'podcast_id': result['podcast_id'],
                'itunesid': result['itunes_id'],
                'description_original': result['description_original'],
                'image': result['image'],
                'info_url': '/podcast/' + result['podcast_id']
            }
        )
    response['results'] = modified_object
    print(response)

    return Response(response=json.dumps(response), status=200, content_type='application/json')


# podcast view
@app.route('/podcast/<podcast_id>')
@login_required
def podcastinfo(podcast_id):
    user_id = current_user.get_id()
    podcast_db = mongo.db.podcasts
    podcast_object = podcast_db.find_one({'podcast_id': podcast_id})
    comment_list = []
    if podcast_object:
        podcast_id = podcast_object['podcast_id']
        podcast_title_original = podcast_object['podcast_title_original']
        description_original = podcast_object['description_original']
        podcast_itunes = podcast_object['itunes_id']
        image = podcast_object['image']
        audio = podcast_object['audio']
        # get comments. If the podcast is in the DB, then at least one comment exists
        comment_db = mongo.db.comments
        comment_object = comment_db.find({'podcast_id': podcast_id}).sort('date_posted', pymongo.ASCENDING)
        # display each comment
        users = mongo.db.users
        for comment in comment_object:
            comment_user_id = comment['user_id']
            user_json = users.find_one({'_id': ObjectId(comment_user_id)})
            user_name = user_json['username']
            comment_list.append({   
                'user_name': user_name,
                'text': comment['text'],
                'date': comment['date_posted'].strftime("%m/%d/%Y %H:%M:%S")
            })
    # If not found, get the podcast data from ListenNotes and create a new DB object
    else: