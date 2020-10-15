import os

from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} # upper- and lower-case checked

app = Flask(__name__, static_url_path="/images")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/image/<img>')
def send_image(img):
    return send_from_directory(app.config['UPLOAD_FOLDER'], img)

@app.route('/')
def index():
    for root, dirs, images in os.walk(app.config['UPLOAD_FOLDER']):
        images.sort()
        
    return render_template('index.html', images=images)

@app.route('/', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        flash('no file part')
        return redirect(url_for('index'))

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        flash('no selected file')
        return redirect(url_for('index'))

    if uploaded_file and allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return redirect(url_for('index'))
