from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3

# Assuming you have a Blueprint set up for dishes
dishes = Blueprint('dishes', __name__)

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to view and add dishes
@dishes.route('/dashboard/dishes', methods=['GET', 'POST'])
def dishes_adm():
    if request.method == 'POST':
        # Fetch dish details from the form
        name = request.form['name']
        description = request.form.get('description')
        availability = request.form['availability']
        if request.form['availability'] == 'on':
            availability = "Available"
        else:
            availability = "Unavailable"
        photo_url = request.form.get('photo_url')

        # Insert dish into the database
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO dish (Name, Description, Availability, Photo_url)
                VALUES (?, ?, ?, ?)
            ''', (name, description, availability, photo_url))
            conn.commit()
            flash('Dish added successfully!')
            return redirect(url_for('dishes.dishes_adm'))
        except sqlite3.IntegrityError:
            flash('Error: Could not add the dish.')
        finally:
            conn.close()

    else:
        # Ensure user is logged in and has admin rights
        if 'user' not in session:
            flash('Please log in first.')
            return redirect(url_for('users.login'))

        if session.get('user')['rol'] == 'ADMIN':
            conn = get_db_connection()
            dishes = conn.execute('SELECT * FROM dish').fetchall()

            # Create a dictionary to hold ingredients for each dish
            dishes_with_ingredients = []
            for dish in dishes:
                dish_ingredients = conn.execute('''
                            SELECT ingredient.Name
                            FROM ingredient
                            JOIN dish_ingredient ON ingredient.ID = dish_ingredient.IngredientID
                            WHERE dish_ingredient.DishID = ?
                        ''', (dish['ID'],)).fetchall()

                # Store dish info and ingredients together
                dishes_with_ingredients.append({
                    "dish": dish,
                    "ingredients": [ingredient["Name"] for ingredient in dish_ingredients]
                })

            conn.close()
            return render_template("admin/dishes/manage.html", dishes_with_ingredients=dishes_with_ingredients)

        else:
            return redirect(url_for('menus.menu'))

# Route to delete a dish
@dishes.route('/dashboard/dishes/<dish_id>/delete', methods=['POST'])
def delete_dish(dish_id):
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('users.login'))

    if session.get('user')['rol'] == 'ADMIN':
        conn = get_db_connection()
        conn.execute('DELETE FROM dish WHERE ID = ?', (dish_id,))
        conn.execute('DELETE FROM dish_ingredient WHERE DishID = ?', (dish_id,))
        conn.commit()
        conn.close()
        flash('Dish deleted.')
        return redirect(url_for('dishes.dishes_adm'))

# Route to edit a dish
@dishes.route('/dashboard/dishes/<dish_id>/edit', methods=['GET', 'POST'])
def edit_dish(dish_id):
    if request.method == 'POST':
        # Ensure user is logged in and has admin rights
        if 'user' not in session:
            flash('Please log in first.')
            return redirect(url_for('users.login'))

        if session.get('user')['rol'] == 'ADMIN':
            conn = get_db_connection()
            name = request.form['name']
            description = request.form.get('description')
            availability = request.form['availability']
            photo_url = request.form.get('photo_url')

            # Update dish in the database
            conn.execute('''
                UPDATE dish
                SET Name = ?, Description = ?, Availability = ?, Photo_url = ?
                WHERE ID = ?
            ''', (name, description, availability, photo_url, dish_id))
            conn.commit()
            conn.close()
            flash('Dish updated.')
            return redirect(url_for('dishes.dishes_adm'))
    else:
        # Display dish details for editing
        if 'user' not in session:
            flash('Please log in first.')
            return redirect(url_for('users.login'))

        if session.get('user')['rol'] == 'ADMIN':
            conn = get_db_connection()
            dish = conn.execute('SELECT * FROM dish WHERE ID = ?', (dish_id,)).fetchone()
            conn.close()
            return render_template("admin/dishes/edit.html", dish=dish)

# Route to manage dish ingredients
@dishes.route('/dashboard/dishes/<dish_id>/ingredients', methods=['GET', 'POST'])
def manage_dish_ingredients(dish_id):
    if 'user' not in session:
        flash('Please log in first.')
        return redirect(url_for('users.login'))

    if session.get('user')['rol'] == 'ADMIN':
        conn = get_db_connection()
        if request.method == 'POST':
            ingredient_id = request.form['ingredient_id']
            conn.execute('''
                INSERT INTO dish_ingredient (DishID, IngredientID)
                VALUES (?, ?)
            ''', (dish_id, ingredient_id))
            conn.commit()
            flash('Ingredient added to dish.')
            return redirect(url_for('dishes.manage_dish_ingredients', dish_id=dish_id))

        # Fetch dish details and available ingredients
        dish = conn.execute('SELECT * FROM dish WHERE ID = ?', (dish_id,)).fetchone()
        ingredients = conn.execute('SELECT * FROM ingredient').fetchall()
        dish_ingredients = conn.execute('''
            SELECT ingredient.*
            FROM ingredient
            JOIN dish_ingredient ON ingredient.ID = dish_ingredient.IngredientID
            WHERE dish_ingredient.DishID = ?
        ''', (dish_id,)).fetchall()
        conn.close()
        return render_template("admin/dishes/ingredients.html", dish=dish, ingredients=ingredients, dish_ingredients=dish_ingredients)
