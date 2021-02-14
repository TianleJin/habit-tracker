from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
import sqlite3

db_path = 'app.db'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

    def validate_username(self, username):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT username FROM user where username = ?", (username.data, ))
        res = cur.fetchone()
        if res is None:
            raise ValidationError('That username does not exist.')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Your passwords do not match.')
    ])
    confirm = PasswordField('Confirm', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT username FROM user where username = ?", (username.data, ))
        res = cur.fetchone()
        if res is not None:
            raise ValidationError('That username already exists.')
