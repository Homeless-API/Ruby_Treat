from flask import Blueprint, Flask, request, render_template, url_for, redirect, session
from Data.savedata import connect_to_postgres
from werkzeug.security import check_password_hash  # Used to check hashed passwords

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
            db_connection, cursor = connect_to_postgres("rubytreatdb", "users")


            if db_connection and cursor:
                # Check if the provided username exists in the database
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()

                if user:
                    # Check if the password matches the stored hashed password
                    stored_password_hash = user[2]  # Assuming user[2] contains the hashed password
                    if check_password_hash(stored_password_hash, password):
                        # User found and password is correct, store user ID in session
                        session['user_id'] = user[0]
                        session['user_type'] = user[6]
                        return redirect(url_for('orders.orders'))
                    else:
                        error = {'invalid_err': 'Incorrect password'}

                else:
                    error = {'invalid_err': 'Invalid username or password'}

            else:
                error = {'db_err': 'Database connection error'}

    except Exception as err:
        print(f'Login failed: {err}')
        error = {'err': 'Login failed due to system error'}

    return render_template('login.html', error=error)

# Register blueprint with the Flask app
app.register_blueprint(login_bp)

if __name__ == '__main__':
    app.run(debug=True)
