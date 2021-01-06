import os
from pathlib import Path

from flask import Flask, flash, request, redirect, abort, url_for, render_template, send_from_directory, current_app
from flask import Blueprint
from werkzeug.utils import secure_filename
from urllib.parse import urlparse, urljoin

from photoflask.forms import LoginForm

main = Blueprint('main', __name__)

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

@main.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('main.index'))
    return render_template('login.html', form=form)

@main.route('/image/<img>')
def serve_image(img):
    return send_from_directory(os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER']), img)

@main.route('/')
def index():

    # images sorted in reverse order of upload time, i.e. newest uploads first.
    #upload_dir = os.path.join(url_for('static', filename=current_app.config['UPLOAD_FOLDER']))
    upload_dir = os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER'])
    print(upload_dir)
    images = [x.name for x in sorted(Path(upload_dir).iterdir(), key=os.path.getmtime, reverse=True)]
    return render_template('index.html', images=images)

@main.route('/', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        flash('no file part')
        return redirect(url_for('index'))

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        flash('no selected file')
        return redirect(url_for('main.index'))

    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(current_app.static_folder, current_app.config['UPLOAD_FOLDER'], filename))


    return redirect(url_for('main.index'))
