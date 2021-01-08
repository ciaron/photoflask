from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, MultipleFileField

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class UploadForm(FlaskForm):
    #files = MultipleFileField('File(s) Upload')
    photo = FileField(validators=[FileRequired()])
