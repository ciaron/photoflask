import os

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

pf = Blueprint('pf', __name__)#, url_prefix='365')

# create and configure the app
app = Flask(__name__) #, instance_relative_config=True)
#app.register_blueprint(pf, url_prefix='/365', template_folder='templates')

login = LoginManager(app)
db = SQLAlchemy()

app.config.from_mapping(
    SECRET_KEY='dev',
    SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(app)

migrate = Migrate(app, db)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # upper- and lower-case checked

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

from app import routes, models
