import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(max=50, message='Your username cannot exceed 50 characters.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Your passwords do not match.')
    ])
    confirm = PasswordField('Confirm', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        conn = sqlite3.connect('app.db')
        cur = conn.cursor()
        cur.execute("SELECT username FROM user where username = ?", (username.data, ))
        res = cur.fetchone()
        if res is not None:
            raise ValidationError('That username already exists.')
