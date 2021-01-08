import os
import exifread
from pathlib import Path

from flask import Flask, flash, request, redirect, abort, url_for, render_template, send_from_directory, current_app
from flask import Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin

from app import app,db
from app.models import User, Image
from app.forms import LoginForm, UploadForm

#main = Blueprint('main', __name__)

#UPLOAD_FOLDER = 'images'
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # upper- and lower-case checked

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('User exists, please choose another email address')
        return redirect(url_for('signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)#form.remember_me.data)
        flash('Welcome ' + form.username.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/image/<img>')
def serve_image(img):
    return send_from_directory(os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER']), img)

def getimagedatetaken(path):
    f = open(path, 'rb')
    tags = exifread.process_file(f)
    f.close()

    # a string of the form '2021:01:05 15:31:46', can be used as a sort key
    if 'Image DateTimeOriginal' in tags:
        return tags.get('Image DateTimeOriginal').values
    else:
        return ""

def getimagedescription(path):

    f = open(path, 'rb')
    tags = exifread.process_file(f)
    f.close()

    if 'Image ImageDescription' in tags:
        return tags.get('Image ImageDescription').values
    else:
        return ""

@app.route('/')
def index():

    upload_dir = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER'])
    # images sorted in reverse order of upload time, i.e. newest uploads first.
    #images = [x.name for x in sorted(Path(upload_dir).iterdir(), key=os.path.getmtime, reverse=True)]

    # images sorted in reverse order of time taken, i.e. newest images first.
    #images = [x.name for x in sorted(Path(upload_dir).iterdir(), key=getimagedatetaken, reverse=True)]
    
    images_ = Image.query.all()
    images = [(x.filename, x.datetaken, x.description) for x in images_]    

    form = UploadForm()   

    return render_template('index.html', images=images, form=form)

@app.route('/', methods=['POST'])
@login_required
def upload_file():

    form = UploadForm()

    if form.validate_on_submit():
        uploaded_file = form.photo.data
        filename = secure_filename(uploaded_file.filename)
        print(filename)
        #f.save(os.path.join(
        #    app.instance_path, 'photos', filename
        #))
        #return redirect(url_for('index'))

        fullpath = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(fullpath)

        # add file info to DB
        description = getimagedescription(fullpath)
        #filename = uploaded_file.filename
        datetaken = getimagedatetaken(fullpath)

        # check if filename already exists, don't upload again
        image = Image.query.filter_by(filename=filename).first()
        if image:
           flash('image with that filename already exists')
           return redirect(url_for('index'))

        new_image = Image(filename=filename, description=description, datetaken=datetaken)
        db.session.add(new_image)
        db.session.commit()

    return redirect(url_for('index'))
