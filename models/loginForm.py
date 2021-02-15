import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

    def validate_username(self, username):
        conn = sqlite3.connect('app.db')
        cur = conn.cursor()
        cur.execute("SELECT username FROM user where username = ?", (username.data, ))
        res = cur.fetchone()
        if res is None:
            raise ValidationError('That username does not exist.')
