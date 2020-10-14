from flask import Flask
from flask import request
from flask import redirect, url_for
from flask import render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.py')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('index'))
