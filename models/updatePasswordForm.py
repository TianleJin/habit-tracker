import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class UpdatePasswordForm(FlaskForm):
    oldPassword = PasswordField('oldPassword', validators=[DataRequired()])
    newPassword1 = PasswordField('newPassword1', validators=[
        DataRequired(),
        EqualTo('newPassword2', message='Your new passwords do not match.')
    ])
    newPassword2 = PasswordField('newPassword2', validators=[DataRequired()])
    submit = SubmitField('Update')