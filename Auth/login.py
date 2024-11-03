from flask import Blueprint, Flask, request, jsonify, render_template, url_for, redirect, session
from Data.savedata import connect_to_postgres

app = Flask(__name__)
login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            # Connect to the PostgreSQL database
            db_connection, cursor = connect_to_postgres('Ruby Treat', 'users')

            # Check if the provided username and password match any user record in the database
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user:
                # User found, store user ID in session
                session['user_id'] = user[0]
                session['user_type'] = user[6]
                return redirect(url_for('orders.orders'))

            else:
                # User not found or password incorrect
                error = {'invalid_err': 'Invalid username or password'}

    except Exception as err:
        print(f'Login failed', err)
        error = {'err': 'Login failed'}

    return render_template('login.html')

app.register_blueprint(login_bp)

if __name__ == '__main__':
    app.run(debug=True)
