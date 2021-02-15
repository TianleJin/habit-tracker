import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


class HabitForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), 
        Length(max=50, message='Input cannot exceed 50 characters.')
    ])
    description = StringField('Description', validators=[
        Length(max=100, message='Input cannot exceed 100 characters.')
    ])
    submit = SubmitField('Add')