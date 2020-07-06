import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-should-be-a-secret-string'
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
    MONGO_URI = os.environ.get('MONGO_URI')
    FLASK_RUN_PORT = os.environ.get('FLASK_RUN_PORT')