from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3

# Assuming you have a Blueprint set up for ingredients
ingredients = Blueprint('ingredients', __name__)


# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = sqlite3.Row
    return conn


# Route to view and add ingredients
@ingredients.route('/dashboard/ingredients', methods=['GET', 'POST'])
def ingredients_adm():
    if request.method == 'POST':
        # Fetch ingredient details from the form
        name = request.form['name']
        description = request.form.get('description')
        photo_url = request.form.get('photo_url')
        date_of_delivery = request.form.get('date_of_delivery')
        expiration_date = request.form.get('expiration_date')
        count = request.form.get('count', type=int)

        # Insert ingredient into the database
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO ingredient (Name, Description, Photo_url, DateOfDelivery, ExpirationDate, Count)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, description, photo_url, date_of_delivery, expiration_date, count))
            conn.commit()
            flash('Ingredient added successfully!')
            return redirect(url_for('ingredients.ingredients_adm'))
        except sqlite3.IntegrityError:
            flash('Error: Could not add the ingredient.')
        finally:
            conn.close()

    else:
        # Ensure user is logged in and has admin rights
        if 'user' not in session:
            flash('Please log in first.')
            return redirect(url_for('users.login'))

        if session.get('user')['rol'] == 'ADMIN':
            conn = get_db_connection()
            ingredients = conn.execute('SELECT * FROM ingredient').fetchall()
            conn.close()
            return render_template("admin/ingredients/manage.html", ingredients=ingredients)

        else:
            return redirect(url_for('menus.menu'))


# Route to delete an ingredient
@ingredients.route('/dashboard/ingredients/<ingredient_id>/delete', methods=['POST'])
def delete_ingredient(ingredient_id):
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('users.login'))

    if session.get('user')['rol'] == 'ADMIN':
        conn = get_db_connection()
        conn.execute('DELETE FROM ingredient WHERE ID = ?', (ingredient_id,))
        conn.commit()
        conn.close()
        flash('Ingredient deleted.')
        return redirect(url_for('ingredients.ingredients_adm'))


@ingredients.route('/dashboard/ingredients/<ingredient_id>/change_count', methods=['POST'])
def change_count(ingredient_id):
    if request.method == 'POST':
        # Ensure user is logged in and has admin rights
        if 'user' not in session:
            flash('Please log in first.')
            return redirect(url_for('users.login'))

        if session.get('user')['rol'] == 'ADMIN':
            conn = get_db_connection()
            count = request.form['count']
            conn.execute('''
                            UPDATE ingredient SET Count = ? WHERE ID = ?''', (count, ingredient_id))
            conn.commit()
            conn.close()
            return redirect(url_for('ingredients.ingredients_adm'))

# Route to edit an ingredient
@ingredients.route('/dashboard/ingredients/<ingredient_id>/edit', methods=['GET', 'POST'])
def edit_ingredient(ingredient_id):
    if request.method == 'POST':
        # Ensure user is logged in and has admin rights
        if 'user' not in session:
            flash('Please log in first.')
            return redirect(url_for('users.login'))

        if session.get('user')['rol'] == 'ADMIN':
            conn = get_db_connection()
            name = request.form['name']
            description = request.form.get('description')
            photo_url = request.form.get('photo_url')
            date_of_delivery = request.form.get('date_of_delivery')
            expiration_date = request.form.get('expiration_date')
            count = request.form.get('count', type=int)

            # Update ingredient in the database
            conn.execute('''
                UPDATE ingredient
                SET Name = ?, Description = ?, Photo_url = ?, DateOfDelivery = ?, ExpirationDate = ?, Count = ?
                WHERE ID = ?
            ''', (name, description, photo_url, date_of_delivery, expiration_date, count, ingredient_id))
            conn.commit()
            conn.close()
            flash('Ingredient updated.')
            return redirect(url_for('ingredients.ingredients_adm'))
    else:
        # Display ingredient details for editing
        if 'user' not in session:
            flash('Please log in first.')
            return redirect(url_for('users.login'))

        if session.get('user')['rol'] == 'ADMIN':
            conn = get_db_connection()
            ingredient = conn.execute('SELECT * FROM ingredient WHERE ID = ?', (ingredient_id,)).fetchone()
            conn.close()
            return render_template("admin/ingredients/edit.html", ingredient=ingredient)
