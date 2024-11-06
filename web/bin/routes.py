import sqlite3
from flask import Flask, render_template, redirect, url_for, request, session, flash,  Blueprint
import hashlib


users = Blueprint('users', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = sqlite3.Row
    return conn

@users.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('users.login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.')
        finally:
            conn.close()

    return render_template('register.html')

@users.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('users.dashboard'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@users.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    flash('You have been logged out.')
    return redirect(url_for('users.login'))

@users.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('users.login'))

    if session.get('user')['rol'] == 'ADMIN':
        return render_template("admin_dashboard.html")
    else:
        return render_template("user_dashboard.html")


#############   USER MANAGEMENT

@users.route('/dashboard/users', methods=['GET','POST'])
def users_adm():
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
            return redirect(url_for('users.login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.')
        finally:
            conn.close()

    else:
        if 'user' not in session:
            flash('Please log in first.')
            return redirect(url_for('users.login'))

        if session.get('user')['rol'] == 'ADMIN':
            conn = get_db_connection()
            userss = conn.execute('SELECT * FROM users').fetchall()
            print(userss)
            return render_template("admin/users/manage.html",users=userss)

        else:
            return redirect(url_for('menus.menu'))

@users.route('/dashboard/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('users.login'))

    if session.get('user')['rol'] == 'ADMIN':
        conn = get_db_connection()
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        flash('User deleted.')
        return redirect(url_for('users.users_adm'))


@users.route('/dashboard/users/<user_id>/chan', methods=['POST'])
def change_role(user_id):
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('users.login'))

    if session.get('user')['rol'] == 'ADMIN':
        conn = get_db_connection()
        if (conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()['rol']=="USER"):
            conn.execute('''UPDATE users SET rol = "ADMIN" WHERE id = ?''', (user_id,))
        else:
            conn.execute('''UPDATE users SET rol = "USER" WHERE id = ?''', (user_id,))
            print("ZHOPE")
        conn.commit()
        return redirect(url_for('users.users_adm'))


@users.route('/dashboard/users/<user_id>/edit', methods=['GET','POST'])
def edit_user(user_id):
    if request.method == 'POST':
        if 'user' not in session:
            flash('Please log in first.')
            return redirect(url_for('users.login'))

        if session.get('user')['rol'] == 'ADMIN':
            conn = get_db_connection()
            login = request.form['login']
            password = hash_password(request.form['password'])
            email = request.form['email']
            phone = request.form['phone']

            conn.execute('UPDATE users SET login = ?, email = ?, phone = ?,password = ? WHERE id = ?',(login, email, phone, password, user_id))
            conn.commit()
            flash('User updated.')
            return redirect(url_for('users.users_adm'))

    else:
        conn = get_db_connection()
        user = conn.cursor().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        return render_template('admin/users/edit.html',user=user)








