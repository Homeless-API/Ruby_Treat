from flask import Blueprint, request, render_template, redirect, url_for, flash, Flask
from werkzeug.utils import secure_filename
import os
from Data.savedata import connect_to_postgres
import re

app = Flask(__name__, static_folder='static')
control_bp = Blueprint('control', __name__)

# Define allowed file extensions for images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Set up upload folder
UPLOAD_FOLDER = 'static/images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to validate price input
def validate_price(price):
    return bool(re.match(r'^[0-9]+(?:\.[0-9]+)?$', price))

@control_bp.route('/controls', methods=['GET', 'POST'])
def control():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'food_pic' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['food_pic']
        
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # Get additional form data
        food_name = request.form.get('food_name')
        description = request.form.get('description')
        price = request.form.get('price')
        
        # Validate price input
        if not validate_price(price):
            flash('Invalid price format. Please enter numbers only.')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
    # Secure filename to prevent directory traversal attacks
            filename = secure_filename(file.filename)
            print(filename)
    
    # Save the file to the upload folder
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

    # Replace backslashes with forward slashes in the file path
            file_path = file_path.replace('\\', '/')

            
            # Connect to the PostgreSQL database
            connection, cursor = connect_to_postgres('Ruby Treat', 'menu')
            
            if connection and cursor:
                # Insert menu item into the specified table
                cursor.execute("""
                    INSERT INTO menu (food_name, description, price, food_pic)
                    VALUES (%s, %s, %s, %s)
                """, (food_name, description, price, file_path))
                
                # Commit the transaction and close the connection
                connection.commit()
                cursor.close()
                connection.close()
                
                flash('Menu item added successfully')
                return redirect(url_for('orders.orders'))
            else:
                flash('Database connection failed. Please try again later.')
                return redirect(request.url)
            
        else:
            flash('Invalid file type. Please upload an image file.')
            return redirect(request.url)

    return render_template('control.html')
