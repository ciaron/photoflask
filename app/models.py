from flask_login import UserMixin

from app import db,login

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))

    def get_name():
        return "pom-pom"

    def check_password(password):
        return True

@login.user_loader
def load_user(id):
    return User.query.get(int(id))