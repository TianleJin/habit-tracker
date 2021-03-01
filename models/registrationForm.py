import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from database.userDb import get_user_by_username


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
        if get_user_by_username(username.data):
            raise ValidationError('That username already exists.')
