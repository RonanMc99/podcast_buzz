from flask import render_template, redirect, url_for, request, flash, Response
from flask_login import current_user, login_user, logout_user, login_required
from podcastbuzz import app, mongo, bcrypt
from podcastbuzz.forms import LogonForm, SignupForm
from podcastbuzz.models import User
from podcastbuzz.listen_notes import search_podcast, get_podcast
from bson.objectid import ObjectId
import json
import pymongo
import datetime


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
        podcast_itunes = podcast_object['podcast_itunes']
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
            if user_json:
                user_name = user_json['username']
                if user_id == comment['user_id']:
                    owned = True
                else:
                    owned = False
            else:
                user_name = 'Anonymous'
                owned = False
            comment_list.append({   
                'user_name': user_name,
                'text': comment['text'],
                'date': comment['date_posted'].strftime("%m/%d/%Y %H:%M:%S")
                'owned': owned,
                'commentId': str(comment['_id'])
            })
    # If not found, get the podcast data from ListenNotes and create a new DB object
    else:
        podcast_object = get_podcast(podcast_id)
        podcast_id = podcast_id
        podcast_title_original = podcast_object['title']
        description_original = podcast_object['description']
        podcast_itunes = podcast_object['itunes_id']
        image = podcast_object['image']
        audio = "https://www.listennotes.com/embedded/e/" + str(podcast_object['episodes'][-1]['id'])
        # put this podcast into the DB
        podcast_db.insert_one({
            'podcast_id': podcast_id,
            'podcast_title_original': podcast_title_original,
            'description_original': description_original,
            'podcast_itunes': podcast_itunes,
            'image': image,
            'audio': audio
        })
    # Create the podcast object
    podcast_info = {
        'podcast_id': podcast_id,
        'podcast_title_original': podcast_title_original,
        'description_original': description_original,
        'podcast_itunes': podcast_itunes,
        'image': image,
        'audio': audio,
    }
    # Create a dict to pass to the page template
    result = {
        'podcast_info': podcast_info,
        'comment_list': comment_list
    }
    return render_template('podcast.html', user_id=user_id, podcast_id=podcast_id, dict=result)


# add comment endpoint
@app.route('/add_comment', methods=['POST'])
def add_comment():
    request_data = request.get_json(force=True)
    text = request_data['comment_text']
    podcast_id = request_data['podcast_id']
    user_id = request_data['user_id']
    date_posted = datetime.datetime.utcnow()
    # Create the comments collection
    comment_db = mongo.db.comments
    comment_db.insert_one({
        'user_id': user_id,
        'podcast_id': podcast_id,
        'text': text,
        'date_posted': date_posted
    })
    users = mongo.db.users
    user_json = users.find_one({'_id': ObjectId(user_id)})
    user_name = user_json['username']
    # create response object
    response = {
        'results': "success",
        'status': 200,
        'user_name': user_name,
        'text': text,
        'date': date_posted.strftime("%m/%d/%Y %H:%M:%S"),
        'commentId': str(commentId)
    }
    return Response(response=json.dumps(response), status=200, content_type='application/json')


# edit comment endpoint
@app.route('/edit_comment', methods=['POST'])
def edit_comment():
    request_data = request.get_json(force=True)
    commentId = request_data['commentId'] if 'commentId' in request_data else ''
    text = request_data['text'] if 'text' in request_data else ''
    comment_db = mongo.db.comments
    mycomment = {'_id': ObjectId(commentId)}
    newvalues = {"$set": {"text": text,  "date_posted": datetime.datetime.utcnow()}}
    comment_db.update_one(mycomment, newvalues)
    response = {
            'results': "success",
            'status': 200
        }
    return Response(response=json.dumps(response), status=200, content_type='application/json')


# delete comment endpoint
@app.route("/delete_comment", methods=['POST'])
def delete_comment():
    request_data = request.get_json(force=True)
    commentId = request_data["commentId"] if "commentId" in request_data else ''
    comment_db = mongo.db.comments
    comment_db.delete_one({'_id': ObjectId(commentId)})
    response = {
            'results': "success",
            'status': 200
        }
    return Response(response=json.dumps(response), status=200, content_type='application/json')
