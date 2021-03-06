from podcastbuzz import login_manager, mongo
from bson.objectid import ObjectId
from flask_login import UserMixin


# Use Flask_login to manage user sessions
@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.users
    user_json = users.find_one({'_id': ObjectId(user_id)})
    return User(user_json)


# UserMixIn provides default implementations for the methods
# that Flask-Login expects user objects to have


class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json

    # Without the id property, it is necessary to override get_id()
    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)
