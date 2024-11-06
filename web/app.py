import sqlite3
from flask import Flask, render_template

from bin.routes import users
from bin.menu import menus
from bin.ingredients import ingredients
from bin.dishes import dishes

app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.register_blueprint(users)
app.register_blueprint(menus)
app.register_blueprint(ingredients)
app.register_blueprint(dishes)

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
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ingredient (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Description TEXT,
        Photo_url TEXT,
        DateOfDelivery DATE,
        ExpirationDate DATE,
        Count INTEGER NOT NULL
        );''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS dish (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Description TEXT,
            Availability TEXT NOT NULL,
            Photo_url TEXT
        );''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS dish_ingredient (
            DishID INTEGER,
            ingredientID INTEGER,
            FOREIGN KEY (DishID) REFERENCES Dish(ID),
            FOREIGN KEY (ingredientID) REFERENCES ingredient(ID),
            PRIMARY KEY (DishID, ingredientID)
        );''')
    conn.execute('''  
        CREATE TABLE IF NOT EXISTS orders (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER NOT NULL,
            DateTimeOfOrder DATETIME NOT NULL,
            ReservationDate DATE,
            DeliveryAddress TEXT,
            Status TEXT NOT NULL
        );''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS order_dish (
            OrderID INTEGER,
            DishID INTEGER,
            FOREIGN KEY (OrderID) REFERENCES orders (ID),
            FOREIGN KEY (DishID) REFERENCES dish(ID),
            PRIMARY KEY (OrderID, DishID)
        ); ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
	init_db()
	app.run(debug=True)
