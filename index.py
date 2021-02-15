import os
import sqlite3
from flask import Flask
from flask import render_template, redirect, url_for, request, flash, get_flashed_messages, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models.loginForm import LoginForm
from models.registrationForm import RegistrationForm
from models.habitForm import HabitForm
from models.user import User

db_path = 'app.db'
user_table = 'user'
habit_table = 'habit'

app = Flask(__name__)
app.secret_key = os.environ['HABIT_TRACKER_SECRET_KEY']

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute(f'SELECT * from {user_table} where user_id = ?', (user_id, ))
    lu = curs.fetchone()
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
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM {user_table} WHERE username = ?', (form.username.data, ))
        res = list(cur.fetchone())
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
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        hsh = generate_password_hash(form.password.data, 'sha256')
        cur.execute(f'INSERT INTO {user_table} (username, password) VALUES (?, ?);', (form.username.data, hsh))
        conn.commit()
        flash('Your account has been created.', category='success')
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

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = HabitForm()
    if form.validate_on_submit():
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f'INSERT INTO {habit_table} (name, description, user_id) VALUES (?, ?, ?);', 
        (form.name.data, form.description.data, current_user.user_id))
        conn.commit()
        flash(f'Your habit "{form.name.data}" has been added.', category='success')
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