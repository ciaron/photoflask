import os
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from sqlalchemy import event
from app import db, login

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    filename = db.Column(db.String(100))
    datetaken = db.Column(db.String(100))
    description = db.Column(db.String(1000)) 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@event.listens_for(User.__table__, 'after_create')
def create_admin_user(*args, **kwargs):

    try:
        email = os.environ['EMAIL']
    except KeyError:
        print("$EMAIL not set")
        sys.exit(1)

    try:
        password = os.environ['PASSWORD']
    except KeyError:
        print("$PASSWORD not set")
        sys.exit(1)

    try:
        username = os.environ['USERNAME']
    except KeyError:
        print("$USERNAME not set")
        sys.exit(1)

    db.session.add(User(email=email, username=username, password=generate_password_hash(password, method='sha256')))
    db.session.commit()
