import os
from flask import Flask
from flask import render_template, redirect, url_for, request, flash, get_flashed_messages, session
import sqlite3
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import LoginForm, RegistrationForm
from users import User

db_path = 'app.db'

app = Flask(__name__)
app.secret_key = os.environ['HABIT_TRACKER_SECRET_KEY']

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute("SELECT * from user where user_id = ?", (user_id, ))
    lu = curs.fetchone()
    return None if lu is None else User(int(lu[0]), lu[1], lu[2])

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE username = ?", (form.username.data, ))
        res = list(cur.fetchone())
        user = load_user(res[0])
        if form.password.data == user.password:
            login_user(user, remember=form.remember.data)
            # print(session.keys())
            # print(form.remember.data)
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
        cur.execute('INSERT INTO user (username, password) VALUES (?, ?);', (form.username.data, form.password.data))
        conn.commit()
        # use this code to check if user was inserted correctly
        # cur.execute('SELECT * FROM user;')
        # print(cur.fetchall())
        flash('Your account has been created.', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    print(session.keys())
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)