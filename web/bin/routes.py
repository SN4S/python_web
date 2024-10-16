import sqlite3
from json import dump

from flask import Flask, render_template, redirect, url_for, request, session, flash,  Blueprint
import hashlib


routes = Blueprint('routes', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = sqlite3.Row
    return conn

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (login, password, email, phone) VALUES (?, ?, ?, ?)',
                         (login, hash_password(password), email, phone))
            conn.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('routes.login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.')
        finally:
            conn.close()

    return render_template('register.html')

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        conn = get_db_connection()
        user_row = conn.execute('SELECT * FROM users WHERE login = ?', (login,)).fetchone()
        conn.close()

        if user_row:
            user = dict(user_row)  # Convert the Row object to a dictionary
            if user['password'] == hash_password(password):
                session['user'] = user # Store the username in the session
                flash('Login successful!')
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@routes.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    flash('You have been logged out.')
    return redirect(url_for('routes.login'))

@routes.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('routes.login'))

    if session.get('user')['rol'] == 'ADMIN':
        return render_template("admin_dashboard.html")
    else:
        return render_template("user_dashboard.html")

@routes.route('/')
def index():
    return render_template("index.html")

@routes.route('/about')
def about():
    return render_template("about.html")