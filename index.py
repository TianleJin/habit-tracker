import os
import sqlite3

from flask import Flask
from flask import render_template, redirect, url_for, make_response, request, flash, get_flashed_messages, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from database.userDb import get_user_by_id, get_user_by_username, insert_user_into_db
from database.habitDb import get_all_habits_for_user, insert_habit_for_user, delete_habit_for_user

from models.loginForm import LoginForm
from models.registrationForm import RegistrationForm
from models.habitForm import HabitForm
from models.user import User

app = Flask(__name__)
app.secret_key = os.environ['HABIT_TRACKER_SECRET_KEY']

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    lu = get_user_by_id(user_id)
    return None if lu is None else User(int(lu[0]), lu[1], lu[2])

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        res = list(get_user_by_username(form.username.data))
        user = load_user(res[0])

        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Your username or password is incorrect.', category='danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if insert_user_into_db(form.username.data, generate_password_hash(form.password.data, 'sha256')):
            flash('Your account has been created.', category='success')
        else:
            flash('Internal server error! Please try again later.', category='danger')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/habit')
def habit():
    habits = get_all_habits_for_user(current_user.user_id)
    return render_template('habit.html', title='Habits', habits=habits)


@app.route('/habit/<habit_id>/delete', methods=['POST'])
@login_required
def delete_habit(habit_id):
    if delete_habit_for_user(current_user.user_id, habit_id):
        return make_response('Your habit has been successfully deleted.', 200) 
    else:
        return make_response('An error has occurred.', 404)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = HabitForm()
    if form.validate_on_submit():
        if insert_habit_for_user(current_user.user_id, form.name.data, form.description.data):
            flash(f'Your habit "{form.name.data}" has been added.', category='success')
        else:
            flash('An error has occurred. Please try again later.', category='danger')
        return redirect(url_for('add'))
    return render_template('add.html', title='Add', form=form)

@app.route('/progress')
@login_required
def progress():
    return render_template('progress.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)