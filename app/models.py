from app import db, login_manager
from passlib.hash import scrypt
from flask_login import UserMixin

from datetime import datetime

class Feedback(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)

#lab6

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean) 
    description = db.Column(db.Boolean)


#lab 8

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


#lab7

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    about_me = db.Column(db.String(240))
    last_seen = db.Column(db.DateTime, default=datetime.now)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = scrypt.hash(password)

    def verify_password(self, pwd):
        return scrypt.verify(pwd, self.password)
    


