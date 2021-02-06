from flask import Flask, render_template, redirect, url_for, request, session, flash, get_flashed_messages
app = Flask(__name__)
app.secret_key = 'abcdefghijklmnopqrstuvwxyz'

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
        # flash('Your username or password is incorrect.')
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # flash('That username has already been taken.')
        # flash('Your passwords do not match.')
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)