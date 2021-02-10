from flask import Flask, render_template, redirect, url_for, request, session, flash, get_flashed_messages, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'abcdefghijklmnopqrstuvwxyz'
DATABASE = 'user.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        # g.db.execute('''CREATE TABLE users (
        #                 username TEXT NOT NULL PRIMARY KEY,
        #                 password TEXT NOT NULL
        #             );''')
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cur = get_db().cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (request.form['username'], ))
        res = cur.fetchone()
        if res and res[1] == request.form['password']:
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        flash('Your username or password is incorrect.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (request.form['username'], ))
        res = cur.fetchone()
        if res:
            flash('That username has already been taken.')
        elif not request.form['username']:
            flash('You must provide a username.')
        elif not request.form['password']:
            flash('You must provide a password.')
        elif request.form['password'] != request.form['confirm']:
            flash('Your passwords do not match.')
        else:
            cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (request.form['username'], request.form['password']))
            conn.commit()
            session['username'] = request.form['username']
            return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)