import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from wtforms.widgets import TextArea


class HabitForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), 
        Length(max=15, message='Habit name cannot exceed 15 characters.')
    ])
    description = StringField('Description', validators=[
        Length(max=50, message='Habit description cannot exceed 50 characters.')
    ], widget=TextArea())
    submit = SubmitField('Add')