import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

#from app import routes, models

db = SQLAlchemy()

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
login = LoginManager(app)

#from app.models import User
#@login.user_loader
#def load_user(user_id):
#    return User.get(user_id)

app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite',
)

db.init_app(app)
migrate = Migrate(app, db)

app.config.from_pyfile('config.py', silent=True)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # upper- and lower-case checked

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
#app.register_blueprint(stream.main)

from app import routes, models
