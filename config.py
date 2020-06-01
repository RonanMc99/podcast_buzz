import os

# set required configuration items as class variables
class Config(object):
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-should-be-a-secret-string'