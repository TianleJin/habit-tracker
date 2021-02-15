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

    def validate_name(self, name):
        conn = sqlite3.connect('app.db')
        cur = conn.cursor()
        cur.execute('SELECT name FROM habit where name = ?', (name.data, ))
        res = cur.fetchone()
        if res is not None:
            raise ValidationError('You have already added this habit.')
