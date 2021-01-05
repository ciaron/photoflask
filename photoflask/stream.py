import os
from pathlib import Path

from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, current_app
from flask import Blueprint
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

#UPLOAD_FOLDER = 'images'
#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # upper- and lower-case checked

#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

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
