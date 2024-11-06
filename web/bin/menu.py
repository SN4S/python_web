import sqlite3
from flask import Flask, render_template, redirect, url_for, request, session, flash,  Blueprint
menus = Blueprint('menus', __name__)

def get_db_connection():
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_available_dishes():
    query='''
                SELECT d.*
                FROM dish d
                JOIN dish_ingredient di ON d.ID = di.DishID
                JOIN ingredient i ON di.ingredientID = i.ID
                GROUP BY d.ID
                HAVING MIN(i.Count) > 0;
            '''

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    dishes = cursor.fetchall()
    conn.close()
    return dishes
@menus.route('/')
def index():
    return render_template("index.html")

@menus.route('/menu')
def menu():
    dishes = get_available_dishes()

    print(dishes)

    return render_template("menu.html", dishes=dishes)


@menus.route('/about')
def about():
    return render_template("about.html")