from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime

orders = Blueprint('orders', __name__)


# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('sqlite.db')
    conn.row_factory = sqlite3.Row
    return conn


# Orders page to view all orders and edit them
@orders.route('/dashboard/orders', methods=['GET', 'POST'])
def orders_adm():
    conn = get_db_connection()

    if request.method == 'POST':
        # Handle order editing
        order_id = request.form['order_id']
        status = request.form.get('status')
        delivery_address = request.form.get('delivery_address')
        reservation_date = request.form.get('reservation_date')

        # Update order details
        conn.execute('''
            UPDATE orders
            SET Status = ?, DeliveryAddress = ?, ReservationDate = ?
            WHERE ID = ?
        ''', (status, delivery_address, reservation_date, order_id))
        conn.commit()
        flash('Order updated successfully!')
        return redirect(url_for('orders.orders_adm'))

    # Get all orders and their dishes
    orders_data = conn.execute('''
        SELECT o.ID, o.UserID, o.DateTimeOfOrder, o.ReservationDate, o.DeliveryAddress, o.Status,
               GROUP_CONCAT(d.Name, ', ') AS Dishes
        FROM orders o
        LEFT JOIN order_dish od ON o.ID = od.OrderID
        LEFT JOIN dish d ON od.DishID = d.ID
        GROUP BY o.ID
    ''').fetchall()
    conn.close()

    return render_template("admin/order/manage.html", orders=orders_data)


# Route to delete an order
@orders.route('/dashboard/orders/<order_id>/delete', methods=['POST'])
def delete_order(order_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM orders WHERE ID = ?', (order_id,))
    conn.commit()
    conn.close()
    flash('Order deleted.')
    return redirect(url_for('orders.orders_adm'))
