import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'secret'
SESSION_PERMANENT = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'var/app-instance/data.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False