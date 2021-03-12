import os
from datetime import datetime, timedelta
import sqlite3

from flask import Flask
from flask import render_template, redirect, url_for, make_response, jsonify, request, flash, get_flashed_messages, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from database.userDb import get_user_by_id, get_user_by_username, insert_user_into_db
from database.habitDb import get_all_habits_for_user, insert_habit_for_user, delete_habit_for_user, update_habit_for_user
from database.recordDb import (get_all_records_for_user, get_completed_habits_count_for_user, check_record_exists, insert_record_for_habit, 
update_record_for_habit, get_completed_habit_count_grouped_by_habits)

from models.loginForm import LoginForm
from models.registrationForm import RegistrationForm
from models.habitForm import HabitForm
from models.user import User

app = Flask(__name__)
app.secret_key = os.environ['HABIT_TRACKER_SECRET_KEY']

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"

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
        res = get_user_by_username(form.username.data)
        if res is False:
            flash('A server error has occurred.', category='danger')
        else:
            res = list(get_user_by_username(form.username.data))
            user = load_user(res[0])
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash(f'Welcome {user.username}!', 'success')
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
            flash('A server error has occurred.', category='danger')
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
    today = datetime.today().strftime('%Y-%m-%d')
    for habit in get_all_habits_for_user(current_user.user_id):
        if not check_record_exists(habit[0], today):
            insert_record_for_habit(habit[0], today)

    today_habit = get_all_records_for_user(current_user.user_id, today)
    return render_template('home.html', title='today', today=today, today_habit=today_habit)

@app.route('/records')
@login_required
def get_records():
    today = datetime.today().strftime('%Y-%m-%d')
    records = get_all_records_for_user(current_user.user_id, today)
    records = [{
        'record_date': record_date,
        'habit_name': habit_name,
        'habit_id': habit_id,
        'status': status 
    } for record_date, habit_name, habit_id, status in records]
    return jsonify(records)

@app.route('/records/update', methods=['POST'])
@login_required
def update_records():
    if update_record_for_habit(request.json['habit_id'], request.json['record_date'], request.json['status']):
        return make_response('success', 200)
    else:
        return make_response('failure', 404)

@app.route('/habit')
@login_required
def habit():
    habits = get_all_habits_for_user(current_user.user_id)
    if habits is False:
        flash('A server error has occurred.', category='danger')
        habits = []
    return render_template('habit.html', title='Habits', habits=habits)

@app.route('/habit/<habit_id>/delete', methods=['POST'])
@login_required
def delete_habit(habit_id):
    if delete_habit_for_user(current_user.user_id, habit_id):
        flash(f'Your habit "{request.form["name"]}" has been deleted.', 'success')
    else:
        flash('A server error has occurred.', 'danger')
    return redirect(url_for('habit'))

@app.route('/habit/<habit_id>/update', methods=['POST'])
@login_required
def update_habit(habit_id):
    if update_habit_for_user(current_user.user_id, habit_id, request.form['desc']):
        flash(f'Your habit "{request.form["name"]}" has been updated.', 'success')
    else:
        flash('A server error has occurred.', 'danger')
    return redirect(url_for('habit'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = HabitForm()
    if form.validate_on_submit():
        if insert_habit_for_user(current_user.user_id, form.name.data, form.description.data):
            flash(f'Your habit "{form.name.data}" has been added.', category='success')
        else:
            flash('An error has occurred.', category='danger')
        return redirect(url_for('add'))
    return render_template('add.html', title='Add', form=form)

@app.route('/progress')
@login_required
def progress():
    return render_template('progress.html', title='Progress')

@app.route('/calendar')
@login_required
def calendar():
    data = get_completed_habits_count_for_user(current_user.user_id)
    return jsonify(create_calendar_json(data))

@app.route('/chart/<start>/<end>')
@login_required
def chart(start, end):
    data = get_completed_habit_count_grouped_by_habits(current_user.user_id, start, end)
    return jsonify(create_chart_data(data))

@app.route('/setting')
@login_required
def setting():
    return render_template('setting.html', title='Setting')

@app.route('/password/update', methods=['POST'])
def update_password():
    return render_template('setting.html', title='Setting')

@app.route('/account/delete', methods=['POST'])
def delete_account():
    return render_template('setting.html', title='Setting')

def create_calendar_json(data):
    today = datetime.now()
    start_date = datetime(today.year, 1, 1)
    end_date = datetime(today.year, 12, 31)

    res = {}
    for x in range(1 + (end_date - start_date).days):
        date = start_date + timedelta(days=x)
        date_string = date.strftime('%Y-%m-%d')
        count = data[date_string] if date_string in data else 0
        time_stamp = round(datetime.timestamp(date))
        res[time_stamp] = count
    return res

def create_chart_data(data):
    res = {}
    for habit_id, habit_name, habit_desc, user_id in get_all_habits_for_user(current_user.user_id):
        res[habit_name] = data[habit_name] if habit_name in data else 0
    return res

if __name__ == '__main__':
    app.run(debug=True)