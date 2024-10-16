import sqlite3
from flask import Flask, render_template

from web.bin.routes import routes

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.register_blueprint(routes)

def get_db_connection():
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            rol TEXT DEFAULT 'USER',
            phone TEXT UNIQUE NOT NULL)''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
	init_db()
	app.run(debug=True)
