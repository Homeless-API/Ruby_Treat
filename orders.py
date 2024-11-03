from flask import Blueprint, render_template
from Data.savedata import connect_to_postgres

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['GET'])
def orders():
    # Connect to the PostgreSQL database
    connection, cursor = connect_to_postgres('Ruby Treat', 'menu')
    
    if connection and cursor:
        # Retrieve menu items from the database
        cursor.execute("SELECT food_name, description, price, food_pic FROM menu")
        menu_items = cursor.fetchall()
        
        # Close the database connection
        cursor.close()
        connection.close()
        
        return render_template('orders.html', menu_items=menu_items)
    else:
        return "Database connection failed. Please try again later."

