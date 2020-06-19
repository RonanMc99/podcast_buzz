from podcast_buzz import login_manager, mongo
from bson.objectid import ObjectId


# Use Flask_login to manage user sessions
@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.users
    user_json = users.find_one({'_id': ObjectId(user_id)})
    return User(user_json)


# UserMixIn provides default implementations for the methods 
# that Flask-Login expects user objects to have


class User(UserMixIn):
    def __init__(self, user_json):
        self.user_json = user_json